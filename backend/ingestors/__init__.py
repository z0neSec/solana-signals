"""Ingestors package for collecting signals from various sources."""
from .onchain import ingest_all as ingest_onchain
from .github import ingest_all as ingest_github
from .social import ingest_all as ingest_social

__all__ = ["ingest_onchain", "ingest_github", "ingest_social"]
