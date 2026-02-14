"""
GitHub ingestor — discovers trending Solana repos and developer activity.
"""
import httpx
import logging
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

GITHUB_API = "https://api.github.com"

SEARCH_QUERIES = [
    "solana agent kit",
    "solana blinks actions",
    "solana DePIN",
    "solana token extensions spl-token-2022",
    "solana compressed nft state-compression",
    "solana intent solver",
    "anchor solana program",
    "solana AI",
    "solana payfi payments",
    "solana restaking",
]


def _headers() -> dict:
    h = {"Accept": "application/vnd.github+json"}
    if settings.github_token:
        h["Authorization"] = f"Bearer {settings.github_token}"
    return h


async def fetch_trending_repos() -> list[dict]:
    """Search GitHub for recently updated Solana-related repos."""
    if not settings.github_token:
        logger.warning("GITHUB_TOKEN not set, skipping GitHub ingestion")
        return []

    signals = []
    cutoff = (datetime.now(timezone.utc) - timedelta(days=14)).strftime("%Y-%m-%d")

    for topic in SEARCH_QUERIES:
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get(
                    f"{GITHUB_API}/search/repositories",
                    headers=_headers(),
                    params={
                        "q": f"{topic} pushed:>{cutoff}",
                        "sort": "updated",
                        "order": "desc",
                        "per_page": 5,
                    },
                )
                if resp.status_code == 200:
                    items = resp.json().get("items", [])
                    for repo in items:
                        try:
                            stars = repo.get("stargazers_count", 0)
                            forks = repo.get("forks_count", 0)
                            # Credibility based on stars
                            cred = min(0.5 + (stars / 500) * 0.5, 0.98)
                            owner = repo.get("owner") or {}

                            signals.append({
                                "id": f"github_repo_{repo['id']}",
                                "domain": "github",
                                "type": "trending_repo",
                                "timestamp": repo.get("pushed_at", datetime.now(timezone.utc).isoformat()),
                                "description": (
                                    f"{repo.get('full_name', 'unknown')} — {(repo.get('description') or 'No description')[:200]} "
                                    f"({stars} stars, {forks} forks)"
                                ),
                                "author": owner.get("login", "unknown"),
                                "source": "github",
                                "url": repo.get("html_url", ""),
                                "metadata": {
                                    "full_name": repo.get("full_name", ""),
                                    "stars": stars,
                                    "forks": forks,
                                    "language": repo.get("language"),
                                    "topics": repo.get("topics", []),
                                    "search_query": topic,
                                    "open_issues": repo.get("open_issues_count", 0),
                                },
                                "credibility_score": round(cred, 2),
                            })
                        except Exception as e:
                            logger.debug(f"Skipping repo: {e}")
                elif resp.status_code == 403:
                    logger.warning("GitHub rate-limited, stopping search")
                    break
                else:
                    logger.debug(f"GitHub search returned {resp.status_code} for '{topic}'")
        except Exception as e:
            logger.error(f"Error searching GitHub for '{topic}': {e}")

    return signals


async def fetch_recent_commits() -> list[dict]:
    """Search for noteworthy recent commits in Solana ecosystem."""
    if not settings.github_token:
        return []

    signals = []
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            # Search recent commits mentioning key Solana terms
            resp = await client.get(
                f"{GITHUB_API}/search/commits",
                headers={**_headers(), "Accept": "application/vnd.github.cloak-preview+json"},
                params={
                    "q": "solana merge:true committer-date:>2024-01-01",
                    "sort": "committer-date",
                    "order": "desc",
                    "per_page": 15,
                },
            )
            if resp.status_code == 200:
                items = resp.json().get("items", [])
                for commit in items:
                    repo_name = commit.get("repository", {}).get("full_name", "")
                    message = commit.get("commit", {}).get("message", "")[:200]
                    author = commit.get("commit", {}).get("author", {})
                    sha = commit.get("sha", "")[:8]

                    signals.append({
                        "id": f"github_commit_{sha}",
                        "domain": "github",
                        "type": "notable_commit",
                        "timestamp": author.get("date", datetime.now(timezone.utc).isoformat()),
                        "description": f"[{repo_name}] {message}",
                        "author": author.get("name", "unknown"),
                        "source": "github",
                        "url": commit.get("html_url", ""),
                        "metadata": {
                            "repo": repo_name,
                            "sha": commit.get("sha", ""),
                            "message": message,
                        },
                        "credibility_score": 0.80,
                    })
    except Exception as e:
        logger.error(f"Error fetching commits: {e}")

    return signals


async def ingest_all() -> list[dict[str, Any]]:
    """Ingest all GitHub signals."""
    logger.info("Ingesting GitHub signals...")
    signals = []

    repos = await fetch_trending_repos()
    signals.extend(repos)

    commits = await fetch_recent_commits()
    signals.extend(commits)

    # Deduplicate
    seen = set()
    unique = []
    for s in signals:
        if s["id"] not in seen:
            seen.add(s["id"])
            unique.append(s)

    logger.info(f"Collected {len(unique)} GitHub signals")
    return unique
