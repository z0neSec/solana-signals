"""
Ingestion coordinator — runs all ingestors and optionally saves signals to Supabase.
"""
import logging
from typing import Any

logger = logging.getLogger(__name__)


async def run_ingestion_pipeline_in_memory() -> list[dict[str, Any]]:
    """
    Run all three ingestors and return raw signals (no DB writes).
    """
    from ingestors import onchain, social, github

    logger.info("🚀 Starting ingestion (in-memory)...")

    onchain_signals = await onchain.ingest_all()
    github_signals = await github.ingest_all()
    social_signals = await social.ingest_all()

    all_signals = onchain_signals + github_signals + social_signals
    logger.info(
        f"📦 Collected {len(all_signals)} signals "
        f"(onchain={len(onchain_signals)}, github={len(github_signals)}, social={len(social_signals)})"
    )
    return all_signals


async def _store_signals(signals: list[dict[str, Any]]) -> int:
    """Try to persist signals to Supabase. Returns number stored."""
    from db.supabase import SignalRepository

    db_rows = []
    for s in signals:
        db_rows.append({
            "id": s["id"],
            "domain": s["domain"],
            "type": s["type"],
            "description": s.get("description", ""),
            "author": s.get("author"),
            "source": s.get("source"),
            "url": s.get("url"),
            "timestamp": s.get("timestamp"),
            "credibility_score": s.get("credibility_score", 0.5),
            "relevance_score": s.get("relevance_score", 0.5),
            "metadata": s.get("metadata", {}),
            "processed": False,
        })

    stored = 0
    chunk_size = 50
    for i in range(0, len(db_rows), chunk_size):
        chunk = db_rows[i : i + chunk_size]
        try:
            SignalRepository.create_many(chunk)
            stored += len(chunk)
        except Exception:
            for row in chunk:
                try:
                    SignalRepository.create(row)
                    stored += 1
                except Exception:
                    pass
    return stored


async def run_ingestion_pipeline() -> dict[str, Any]:
    """Run all ingestors and store signals in Supabase."""
    all_signals = await run_ingestion_pipeline_in_memory()
    stored = await _store_signals(all_signals)

    return {
        "status": "complete",
        "signals_collected": len(all_signals),
        "signals_stored": stored,
    }
