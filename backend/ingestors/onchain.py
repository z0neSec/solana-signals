"""
Onchain data ingestor using Helius API.

Collects:
- New program deployments and activity
- Transaction volume on Solana DeFi/infra programs
- Enhanced transaction data
"""
import httpx
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Any
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

HELIUS_RPC = f"https://mainnet.helius-rpc.com/?api-key={settings.helius_api_key}"
HELIUS_API = f"https://api.helius.xyz/v0"

# Well-known Solana programs to track for narrative signals
TRACKED_PROGRAMS = {
    "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4": "Jupiter Aggregator",
    "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc": "Orca Whirlpool",
    "M2mx93ekt1fmXSVkTrUL9xVFHkmME8HTUi5Cyc5aF7K": "Magic Eden v2",
    "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s": "Metaplex Token Metadata",
    "BGUMAp9Gq7iTEuizy4pqaxsTyUCBK68MDfK752saRPUY": "Bubblegum (cNFTs)",
    "cmtDvXumGCrqC1Age74AVPhSRVXJMd8PJS91L8KbNCK": "State Compression",
    "PhoeNiXZ8ByJGLkxNfZRnkUfjvmuYqLR89jjFHGqdXY": "Phoenix DEX",
    "dRiftyHA39MWEi3m9aunc5MzRF1JYuBsbn6VPcn33UH": "Drift Protocol",
    "MERLuDFBMmsHnsBPZw2sDQZHvXFMwp8EdjudcU2HKky": "Marinade Finance",
    "JitoSo1iCiB4htjGKfGkGbMGLsxo7dkkD4zp7Nkb4w3": "Jito Staking",
}

SOLANA_ECOSYSTEM_SEARCHES = [
    "solana AI agent",
    "solana blinks",
    "solana DePIN",
    "solana compressed NFT",
    "solana intent DEX",
    "solana PayFi",
    "solana restaking",
    "solana token extensions",
]


async def fetch_enriched_transactions(program_id: str, program_name: str) -> list[dict]:
    """Fetch enriched transaction data from Helius for a program."""
    if not settings.helius_api_key:
        logger.warning("HELIUS_API_KEY not set, skipping onchain ingestion")
        return []

    signals = []
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            # Use Helius enhanced API for parsed transactions
            resp = await client.get(
                f"{HELIUS_API}/addresses/{program_id}/transactions",
                params={"api-key": settings.helius_api_key, "limit": 20},
            )
            if resp.status_code == 200:
                txns = resp.json()
                if txns:
                    # Count unique signers as a proxy for user activity
                    signers = set()
                    for tx in txns:
                        if "feePayer" in tx:
                            signers.add(tx["feePayer"])

                    ts = txns[0].get("timestamp", 0)
                    ts_str = datetime.fromtimestamp(ts).isoformat() if ts else datetime.now().isoformat()

                    signals.append({
                        "id": f"onchain_{hashlib.md5(program_id.encode()).hexdigest()[:12]}",
                        "domain": "onchain",
                        "type": "program_activity",
                        "timestamp": ts_str,
                        "description": (
                            f"{program_name} ({program_id[:8]}…) showed {len(txns)} recent transactions "
                            f"from {len(signers)} unique wallets"
                        ),
                        "author": program_name,
                        "source": "helius",
                        "url": f"https://solscan.io/account/{program_id}",
                        "metadata": {
                            "program_id": program_id,
                            "program_name": program_name,
                            "tx_count": len(txns),
                            "unique_wallets": len(signers),
                        },
                        "credibility_score": 0.90,
                    })
            else:
                logger.debug(f"Helius returned {resp.status_code} for {program_name}")
    except Exception as e:
        logger.error(f"Error fetching txns for {program_name}: {e}")

    return signals


async def fetch_recent_token_activity() -> list[dict]:
    """Use Helius DAS (Digital Asset Standard) to find trending tokens/NFTs."""
    if not settings.helius_api_key:
        return []

    signals = []
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            # Get slot to check network health
            resp = await client.post(HELIUS_RPC, json={
                "jsonrpc": "2.0", "id": 1, "method": "getSlot"
            })
            if resp.status_code == 200:
                slot = resp.json().get("result", 0)
                signals.append({
                    "id": f"onchain_slot_{slot}",
                    "domain": "onchain",
                    "type": "network_health",
                    "timestamp": datetime.now().isoformat(),
                    "description": f"Solana network at slot {slot:,} — network is active and processing blocks",
                    "author": "Solana Network",
                    "source": "helius",
                    "url": "https://explorer.solana.com",
                    "metadata": {"slot": slot},
                    "credibility_score": 0.95,
                })

            # Get recent priority fee data as a signal of network demand
            resp2 = await client.post(HELIUS_RPC, json={
                "jsonrpc": "2.0", "id": 2,
                "method": "getRecentPrioritizationFees",
                "params": []
            })
            if resp2.status_code == 200:
                fees = resp2.json().get("result", [])
                if fees:
                    avg_fee = sum(f.get("prioritizationFee", 0) for f in fees[-20:]) / min(20, len(fees))
                    signals.append({
                        "id": f"onchain_fees_{datetime.now().strftime('%Y%m%d%H')}",
                        "domain": "onchain",
                        "type": "fee_activity",
                        "timestamp": datetime.now().isoformat(),
                        "description": f"Average priority fee: {avg_fee:,.0f} micro-lamports — {'high demand' if avg_fee > 10000 else 'normal demand'} period",
                        "author": "Solana Network",
                        "source": "helius",
                        "url": "https://explorer.solana.com",
                        "metadata": {"avg_priority_fee": avg_fee, "sample_size": len(fees)},
                        "credibility_score": 0.92,
                    })
    except Exception as e:
        logger.error(f"Error fetching token activity: {e}")

    return signals


async def ingest_all() -> list[dict[str, Any]]:
    """Ingest all onchain signals from Helius."""
    logger.info("Ingesting onchain signals from Helius...")
    signals = []

    # 1. Fetch activity for tracked programs
    for program_id, program_name in TRACKED_PROGRAMS.items():
        sigs = await fetch_enriched_transactions(program_id, program_name)
        signals.extend(sigs)

    # 2. Fetch network-level data
    network_sigs = await fetch_recent_token_activity()
    signals.extend(network_sigs)

    logger.info(f"Collected {len(signals)} onchain signals")
    return signals
