"""
Processing pipeline — embeds, clusters, scores, and enriches signals into narratives.

Works entirely in-memory: collects signals → embeds → clusters → scores → enriches.
Attempts to persist to Supabase but gracefully handles RLS/auth issues.
"""
import logging
from datetime import datetime, timedelta
from typing import Any
import uuid

logger = logging.getLogger(__name__)

# In-memory cache of last pipeline results so the API can serve them
_cached_signals: list[dict] = []
_cached_narratives: list[dict] = []


def get_cached_signals() -> list[dict]:
    return _cached_signals


def get_cached_narratives() -> list[dict]:
    return _cached_narratives


def _deduplicate_narratives(narratives: list[dict]) -> list[dict]:
    """Merge narratives that share the same label, combining their signals."""
    from collections import OrderedDict

    merged: OrderedDict[str, dict] = OrderedDict()
    for n in narratives:
        label = n.get("label", "Unknown")
        if label in merged:
            existing = merged[label]
            # Merge signal lists
            existing_sigs = existing.get("signals", [])
            new_sigs = n.get("signals", [])
            seen_ids = {s.get("id") for s in existing_sigs}
            for s in new_sigs:
                if s.get("id") not in seen_ids:
                    existing_sigs.append(s)
                    seen_ids.add(s.get("id"))
            existing["signals"] = existing_sigs
            existing["signal_count"] = len(existing_sigs)

            # Merge domains
            all_domains = set(existing.get("domains", []))
            all_domains.update(n.get("domains", []))
            existing["domains"] = sorted(all_domains)

            # Merge domain_counts
            dc = existing.get("domain_counts", {})
            for d, c in n.get("domain_counts", {}).items():
                dc[d] = dc.get(d, 0) + c
            existing["domain_counts"] = dc

            # Keep higher confidence
            if n.get("confidence", 0) > existing.get("confidence", 0):
                existing["confidence"] = n["confidence"]

            # Merge entities
            ent1 = existing.get("entities", {})
            ent2 = n.get("entities", {})
            for key in ("programs", "repos", "kols"):
                combined = list(dict.fromkeys(ent1.get(key, []) + ent2.get(key, [])))
                ent1[key] = combined
            existing["entities"] = ent1

            # Merge evidence
            ev1 = existing.get("evidence", [])
            ev2 = n.get("evidence", [])
            ev_ids = {e.get("signal_id") for e in ev1}
            for e in ev2:
                if e.get("signal_id") not in ev_ids:
                    ev1.append(e)
            existing["evidence"] = ev1

            # Merge build ideas (no dupes by title)
            bi1 = existing.get("build_ideas", [])
            bi2 = n.get("build_ideas", [])
            bi_titles = {b.get("title") for b in bi1}
            for b in bi2:
                if b.get("title") not in bi_titles:
                    bi1.append(b)
            existing["build_ideas"] = bi1

            logger.info(f"🔀 Merged duplicate narrative '{label}' → {existing['signal_count']} signals")
        else:
            merged[label] = n

    # Re-rank
    result = list(merged.values())
    result.sort(key=lambda x: x.get("confidence", 0), reverse=True)
    for i, n in enumerate(result):
        n["rank"] = i + 1

    if len(result) < len(narratives):
        logger.info(f"🧹 Deduplicated {len(narratives)} → {len(result)} narratives")

    return result


async def run_processing_pipeline(signals: list[dict] | None = None) -> dict[str, Any]:
    """
    Run the full processing pipeline.

    If signals are provided, use them directly (in-memory mode).
    Otherwise, try to load from Supabase.
    """
    from processing import embeddings, clustering, scoring, ideas

    logger.info("⚙️  Starting processing pipeline...")

    # 1. Use provided signals or try DB
    if not signals:
        try:
            from db.supabase import SignalRepository
            signals = SignalRepository.get_recent(days=14, limit=500)
        except Exception as e:
            logger.warning(f"Could not load signals from DB: {e}")
            signals = []

    if not signals:
        logger.warning("No signals to process")
        return {"status": "complete", "narratives_created": 0, "signals_processed": 0}

    logger.info(f"📥 Processing {len(signals)} signals")

    # 2. Embed
    embedded = await embeddings.embed_signals(signals)

    # 3. Store vectors in Pinecone (best-effort)
    try:
        await embeddings.store_embeddings_pinecone(embedded)
    except Exception as e:
        logger.warning(f"Pinecone storage failed: {e}")

    # 4. Cluster
    narratives = await clustering.cluster_signals(embedded)
    logger.info(f"🔬 {len(narratives)} clusters detected")

    if not narratives:
        return {"status": "complete", "narratives_created": 0, "signals_processed": len(signals)}

    # 5. Score
    scored = await scoring.score_narratives(narratives)

    # 6. Enrich
    enriched = await ideas.generate_build_ideas(scored)

    # 6b. Deduplicate narratives with identical labels (merge signals)
    enriched = _deduplicate_narratives(enriched)

    # 7. Try to persist to Supabase
    today = datetime.now().date()
    fortnight_start = (today - timedelta(days=14)).isoformat()

    created_count = 0
    for narrative in enriched:
        # Convert confidence from 0-1 → 0-100 for DB constraint
        raw_confidence = narrative.get("confidence", 0)
        db_confidence = round(raw_confidence * 100, 1) if raw_confidence <= 1 else raw_confidence

        narrative["_db_row"] = {
            "id": narrative.get("id", f"narrative_{uuid.uuid4().hex[:12]}"),
            "label": narrative.get("label", "Emerging Trend"),
            "summary": narrative.get("summary", ""),
            "status": narrative.get("status", "NEW"),
            "confidence": db_confidence,
            "rank": narrative.get("rank", 99),
            "signal_count": narrative.get("signal_count", 0),
            "domains": narrative.get("domains", []),
            "domain_counts": narrative.get("domain_counts", {}),
            "first_seen": narrative.get("first_seen"),
            "last_seen": narrative.get("last_seen"),
            "scores": narrative.get("scores", {}),
            "build_ideas": narrative.get("build_ideas", []),
            "entities": narrative.get("entities", {}),
            "evidence": narrative.get("evidence", []),
            "why_now": narrative.get("why_now"),
            "comparable_precedent": narrative.get("comparable_precedent"),
            "fortnight_start": fortnight_start,
        }

        try:
            from db.supabase import NarrativeRepository, SignalRepository
            NarrativeRepository.create(narrative["_db_row"])
            created_count += 1

            # Link signals
            for sig in narrative.get("signals", []):
                try:
                    SignalRepository.update(sig["id"], {
                        "narrative_id": narrative["_db_row"]["id"],
                        "processed": True,
                    })
                except Exception:
                    pass
        except Exception as e:
            logger.debug(f"DB write skipped for {narrative.get('label')}: {e}")

    # 8. Cache results in memory so the API can serve them
    global _cached_signals, _cached_narratives
    _cached_signals = signals
    # Build API-friendly narrative objects
    _cached_narratives = []
    for n in enriched:
        db_row = n.get("_db_row", {})
        # Add signals list (without embeddings to save memory)
        row = dict(db_row)
        row["signals"] = [
            {k: v for k, v in s.items() if k != "embedding"}
            for s in n.get("signals", [])
        ]
        _cached_narratives.append(row)

    summary = {
        "status": "complete",
        "narratives_created": created_count,
        "narratives_cached": len(_cached_narratives),
        "signals_processed": len(signals),
        "narrative_labels": [n.get("label", "") for n in enriched],
    }
    logger.info(f"✅ Processing complete: {len(_cached_narratives)} narratives ({created_count} persisted to DB)")
    return summary


async def run_full_pipeline() -> dict[str, Any]:
    """Run ingestion + processing back-to-back, passing signals in memory."""
    from ingestors.coordinator import run_ingestion_pipeline_in_memory

    logger.info("🚀 Running full pipeline (in-memory mode)...")

    # Collect signals
    all_signals = await run_ingestion_pipeline_in_memory()

    # Try to store in DB (best effort)
    stored = 0
    try:
        from db.supabase import SignalRepository
        from ingestors.coordinator import _store_signals
        stored = await _store_signals(all_signals)
    except Exception as e:
        logger.warning(f"DB signal storage skipped: {e}")

    # Process in memory
    process_result = await run_processing_pipeline(all_signals)

    return {
        "ingestion": {
            "status": "complete",
            "signals_collected": len(all_signals),
            "signals_stored": stored,
        },
        "processing": process_result,
    }
