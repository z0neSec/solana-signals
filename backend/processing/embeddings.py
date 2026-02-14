"""
Embedding module — generates vector embeddings for signals.

Uses OpenAI text-embedding-3-small (1536 dims).
Falls back to deterministic hash-based vectors when OpenAI quota is exceeded.
"""
import hashlib
import logging
import numpy as np
from typing import Any

logger = logging.getLogger(__name__)

try:
    from openai import AsyncOpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    from pinecone import Pinecone
    HAS_PINECONE = True
except ImportError:
    HAS_PINECONE = False

from config import get_settings

settings = get_settings()
EMBEDDING_DIM = 1536
EMBEDDING_MODEL = "text-embedding-3-small"


def _deterministic_vector(text: str) -> list[float]:
    """Produce a repeatable 1536-d unit vector from text hash.
    This is NOT a real semantic embedding but keeps clustering possible
    when the OpenAI quota is exhausted.
    """
    seed = int(hashlib.sha256(text.encode()).hexdigest(), 16) % (2**32)
    rng = np.random.RandomState(seed)
    vec = rng.randn(EMBEDDING_DIM).astype(np.float32)
    vec /= np.linalg.norm(vec)
    return vec.tolist()


async def get_embedding(text: str) -> list[float]:
    """Get embedding for a single text. Falls back to hash vector on error."""
    if not HAS_OPENAI or not settings.openai_api_key:
        logger.debug("OpenAI unavailable — using deterministic vector")
        return _deterministic_vector(text)

    try:
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        resp = await client.embeddings.create(model=EMBEDDING_MODEL, input=text)
        return resp.data[0].embedding
    except Exception as e:
        logger.warning(f"OpenAI embedding failed ({e}), using deterministic fallback")
        return _deterministic_vector(text)


async def embed_signals(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Add 'embedding' key to every signal dict."""
    logger.info(f"Generating embeddings for {len(signals)} signals...")

    # Try batch via OpenAI first
    texts = [s.get("description", "") for s in signals]

    if HAS_OPENAI and settings.openai_api_key:
        try:
            client = AsyncOpenAI(api_key=settings.openai_api_key)
            # OpenAI batch limit is 2048 texts
            batch_size = 256
            all_embeddings: list[list[float]] = []
            for i in range(0, len(texts), batch_size):
                batch = texts[i : i + batch_size]
                resp = await client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
                all_embeddings.extend([d.embedding for d in resp.data])

            for sig, emb in zip(signals, all_embeddings):
                sig["embedding"] = emb

            logger.info("Used OpenAI embeddings")
            return signals
        except Exception as e:
            logger.warning(f"OpenAI batch embed failed ({e}), falling back to hash vectors")

    # Fallback — deterministic vectors
    for sig in signals:
        sig["embedding"] = _deterministic_vector(sig.get("description", ""))

    logger.info("Used deterministic fallback embeddings")
    return signals


async def store_embeddings_pinecone(signals: list[dict[str, Any]]) -> int:
    """Upsert signal embeddings into Pinecone index. Returns count stored."""
    if not HAS_PINECONE or not settings.pinecone_api_key:
        logger.info("Pinecone not configured — skipping vector store")
        return 0

    try:
        pc = Pinecone(api_key=settings.pinecone_api_key)
        idx = pc.Index(settings.pinecone_index_name or "solana-signals")

        vectors = []
        for s in signals:
            if "embedding" not in s:
                continue
            vectors.append({
                "id": s["id"],
                "values": s["embedding"],
                "metadata": {
                    "domain": s.get("domain", ""),
                    "type": s.get("type", ""),
                    "description": s.get("description", "")[:400],
                    "timestamp": s.get("timestamp", ""),
                },
            })

        # Upsert in batches of 100
        batch = 100
        stored = 0
        for i in range(0, len(vectors), batch):
            idx.upsert(vectors=vectors[i : i + batch])
            stored += len(vectors[i : i + batch])

        logger.info(f"📌 Stored {stored} vectors in Pinecone")
        return stored
    except Exception as e:
        logger.error(f"Pinecone upsert failed: {e}")
        return 0
