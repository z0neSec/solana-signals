"""
Ideas & label generation for detected narratives.

Uses GPT-4 when available, otherwise applies keyword-based heuristics.
"""
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

try:
    from openai import AsyncOpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

from config import get_settings

settings = get_settings()

# ── Keyword-based label mapping ──────────────────────────────────────────────
LABEL_KEYWORDS: list[tuple[list[str], str]] = [
    (["agent", "ai agent", "sendai", "rig", "eliza"], "AI Agents on Solana"),
    (["blink", "actions", "dialect"], "Solana Blinks & Actions"),
    (["depin", "helium", "hivemapper", "iot", "render"], "DePIN Infrastructure"),
    (["compressed", "cnft", "bubblegum", "state compression"], "Compressed NFTs / State Compression"),
    (["intent", "solver", "order flow"], "Intent-Based Trading"),
    (["token extension", "spl-token-2022", "transfer hook", "confidential"], "Token Extensions (SPL-2022)"),
    (["restaking", "liquid staking", "jito", "marinade", "sanctum"], "Liquid Staking & Restaking"),
    (["payfi", "payment", "pay", "sphere", "helio"], "PayFi & Payments"),
    (["jupiter", "jup", "dex", "swap", "aggregator"], "DEX & Aggregation"),
    (["drift", "perp", "futures", "leverage"], "Perpetuals & Derivatives"),
    (["nft", "metaplex", "magic eden", "tensor"], "NFT Ecosystem"),
    (["mobile", "saga", "chapter 2", "dapp store"], "Solana Mobile"),
    (["firedancer", "validator", "client diversity"], "Validator & Client Diversity"),
    (["governance", "realms", "dao"], "DAO & Governance"),
    (["gaming", "star atlas", "aurory"], "Gaming on Solana"),
    (["phoenix", "orderbook", "clob"], "On-Chain Orderbooks"),
]

# ── Fallback build ideas ────────────────────────────────────────────────────
FALLBACK_BUILD_IDEAS: dict[str, list[dict]] = {
    "AI Agents on Solana": [
        {
            "title": "Agent Launchpad",
            "description": "No-code platform to deploy AI agents that execute on-chain actions via Solana Agent Kit.",
            "problem": "Building autonomous agents on Solana requires deep Rust/Anchor knowledge, limiting who can participate.",
            "solution": "Visual builder + hosted runtime that lets anyone configure agent strategies, connect wallets, and deploy live.",
            "business_model": "Freemium SaaS — free for 1 agent, $49/mo for teams with monitoring and analytics.",
            "effort": "4-6 weeks",
        },
        {
            "title": "Agent Analytics Dashboard",
            "description": "Monitor autonomous agent wallet activity, PnL, and strategy performance in real time.",
            "problem": "No visibility into what AI agents are doing with funds — operators can't debug or optimize strategies.",
            "solution": "Real-time dashboard showing agent transactions, portfolio changes, strategy performance, and alerts.",
            "business_model": "SaaS subscription — $29/mo per agent monitored, enterprise tier for fleet management.",
            "effort": "2-3 weeks",
        },
        {
            "title": "Multi-Agent Orchestrator",
            "description": "Framework for composing multiple AI agents that collaborate on complex DeFi strategies.",
            "problem": "Single agents hit limits on complex tasks like cross-protocol arbitrage or portfolio rebalancing.",
            "solution": "Orchestation layer where specialized agents (research, execution, risk) coordinate via message passing.",
            "business_model": "Open-source framework with managed cloud offering — usage-based pricing per agent-hour.",
            "effort": "6-8 weeks",
        },
        {
            "title": "Scoped Wallet Delegation",
            "description": "On-chain program for granular permission delegation — spend limits, allowed programs, time bounds.",
            "problem": "Agents need wallet access but full private key exposure is risky for high-value operations.",
            "solution": "Smart contract that issues scoped session keys with configurable constraints (max spend, program whitelist, expiry).",
            "business_model": "Protocol fee on delegated transactions (0.01%), plus enterprise licensing.",
            "effort": "3-4 weeks",
        },
    ],
    "Solana Blinks & Actions": [
        {
            "title": "Blink Storefront",
            "description": "Embeddable commerce widget powered by Blinks — one-click checkout on any website.",
            "problem": "Merchants want crypto payments but integration is complex and users abandon multi-step flows.",
            "solution": "Drop-in JS widget that renders as a Blink — users transact in one click without leaving the page.",
            "business_model": "1% transaction fee, waived for first $10K/mo. Premium tier with analytics.",
            "effort": "2-3 weeks",
        },
        {
            "title": "Social Blinks SDK",
            "description": "React library to embed tipping, swaps, and minting directly in social feeds.",
            "problem": "Social platforms don't natively support on-chain actions, requiring users to leave the app.",
            "solution": "React component library that renders interactive Blinks for tips, swaps, and mints inline in any feed.",
            "business_model": "Open-source SDK, monetize via hosted relay infrastructure ($0.001/tx).",
            "effort": "2 weeks",
        },
        {
            "title": "Blink Analytics",
            "description": "Track conversion rates, engagement, and revenue for deployed Blinks across platforms.",
            "problem": "Blink creators have no visibility into how their links perform — clicks, completions, drop-off.",
            "solution": "Analytics dashboard that tracks Blink impressions, click-through, transaction completion, and A/B testing.",
            "business_model": "Freemium — free for 5 Blinks, $19/mo for unlimited with advanced analytics.",
            "effort": "2-3 weeks",
        },
    ],
    "DePIN Infrastructure": [
        {
            "title": "DePIN Aggregator",
            "description": "Unified dashboard tracking all Solana DePIN networks — coverage maps, earnings, uptime.",
            "problem": "DePIN operators run nodes across Helium, Hivemapper, Render etc. but can't see unified performance.",
            "solution": "Single dashboard aggregating all DePIN networks with coverage maps, earnings calculators, and alerts.",
            "business_model": "Freemium with premium alerts and tax reporting ($9/mo).",
            "effort": "3-4 weeks",
        },
        {
            "title": "Proof-of-Coverage Verifier",
            "description": "Independent tool to audit and verify DePIN coverage claims against real-world data.",
            "problem": "DePIN networks self-report coverage, creating trust issues for buyers and investors.",
            "solution": "Independent verification using satellite data, crowd-sourced testing, and cross-network correlation.",
            "business_model": "B2B SaaS for DePIN protocols and institutional investors — $499/mo.",
            "effort": "6-8 weeks",
        },
        {
            "title": "DePIN Marketplace",
            "description": "Marketplace where users buy DePIN services (compute, storage, bandwidth) with unified billing.",
            "problem": "Buying services from individual DePIN networks requires separate accounts, tokens, and interfaces.",
            "solution": "Unified marketplace with pay-with-USDC, automatic provider selection, and SLA guarantees.",
            "business_model": "10% marketplace fee on transactions.",
            "effort": "4-6 weeks",
        },
    ],
    "Compressed NFTs / State Compression": [
        {
            "title": "Batch Mint API",
            "description": "Developer API to mint millions of compressed NFTs for loyalty, tickets, or credentials.",
            "problem": "Minting millions of NFTs is expensive and complex even with compression — devs need managed infra.",
            "solution": "REST API that handles Merkle tree creation, minting, and metadata hosting — 1M cNFTs for ~$100.",
            "business_model": "Pay-per-mint pricing (0.0001 SOL/cNFT) with volume discounts.",
            "effort": "3-4 weeks",
        },
        {
            "title": "cNFT Explorer",
            "description": "Block explorer optimised for browsing and searching compressed NFT collections.",
            "problem": "Standard explorers don't index compressed NFTs well — users can't find, verify, or trade them.",
            "solution": "Specialized explorer with collection browsing, ownership verification, and transfer history for cNFTs.",
            "business_model": "Ad-supported free tier, premium API access for developers ($29/mo).",
            "effort": "2-3 weeks",
        },
        {
            "title": "Loyalty cNFT Platform",
            "description": "White-label loyalty program using compressed NFTs — brands issue rewards at near-zero cost.",
            "problem": "Traditional loyalty programs are siloed, points expire, and infrastructure costs are high.",
            "solution": "Platform where brands mint loyalty cNFTs (pennies each), customers collect cross-brand, trade freely.",
            "business_model": "SaaS for brands — $199/mo + $0.001/mint. Consumer app is free.",
            "effort": "4-5 weeks",
        },
    ],
    "Token Extensions (SPL-2022)": [
        {
            "title": "Transfer Hook Marketplace",
            "description": "Registry of audited transfer hook programs that token issuers can plug-and-play.",
            "problem": "Writing custom transfer hooks requires Rust expertise and expensive audits.",
            "solution": "Curated marketplace of pre-audited hooks (royalty enforcement, KYC gates, tax withholding) ready to attach.",
            "business_model": "Listing fee for hook authors + usage royalty (0.1% of transfer value).",
            "effort": "4-6 weeks",
        },
        {
            "title": "Confidential Token Wallet",
            "description": "Wallet with native support for confidential transfer balances and privacy features.",
            "problem": "SPL-2022 confidential transfers exist but no wallet supports them — enterprises can't use them.",
            "solution": "Wallet app (browser extension + mobile) with native privacy mode for confidential token operations.",
            "business_model": "Premium wallet features ($4.99/mo), institutional API licensing.",
            "effort": "6-8 weeks",
        },
        {
            "title": "Token Extension Builder",
            "description": "Visual tool to configure and deploy SPL-2022 tokens with extensions — no code required.",
            "problem": "Creating tokens with transfer hooks, interest rates, or metadata extensions requires CLI expertise.",
            "solution": "Web UI to select extensions, configure parameters, preview behaviour, and deploy with one click.",
            "business_model": "Free for basic tokens, $49/deployment for advanced extensions with audit report.",
            "effort": "3-4 weeks",
        },
    ],
    "Liquid Staking & Restaking": [
        {
            "title": "LST Yield Optimiser",
            "description": "Auto-rotate between mSOL, jitoSOL, bSOL based on real-time APY and risk metrics.",
            "problem": "LST yields fluctuate across protocols but most users park in one and miss better returns.",
            "solution": "Smart vault that continuously rebalances across LSTs based on yield, risk, and liquidity depth.",
            "business_model": "Performance fee — 10% of yield above baseline SOL staking rate.",
            "effort": "3-4 weeks",
        },
        {
            "title": "Restaking Risk Monitor",
            "description": "Dashboard showing exposure, slashing risk, and correlation across restaking protocols.",
            "problem": "Restaking compounds risk — users don't understand their exposure across multiple AVS operators.",
            "solution": "Risk dashboard with slashing probability models, correlation matrices, and position alerts.",
            "business_model": "Freemium — free for personal use, $49/mo for institutions with API access.",
            "effort": "3-4 weeks",
        },
        {
            "title": "LST Portfolio Tracker",
            "description": "Track staking rewards, MEV tips, and airdrop eligibility across all Solana LST positions.",
            "problem": "Users hold multiple LSTs but can't see consolidated rewards, tax events, or airdrop eligibility.",
            "solution": "Portfolio view with reward accrual tracking, tax report export, and airdrop eligibility checker.",
            "business_model": "Free tracking, premium tax reports ($19/year), airdrop alerts ($4.99/mo).",
            "effort": "2-3 weeks",
        },
    ],
    "Intent-Based Trading": [
        {
            "title": "Intent DEX Frontend",
            "description": "User-friendly swap UI that submits intents and lets solvers compete for best execution.",
            "problem": "Current DEX UIs execute trades directly — users get worse prices than what solver competition enables.",
            "solution": "Swap interface where users declare intent (token, amount, deadline) and solvers bid for execution.",
            "business_model": "Solver fee sharing — platform takes 15% of solver spread.",
            "effort": "3-4 weeks",
        },
        {
            "title": "Solver Leaderboard",
            "description": "Track solver fill rates, MEV extraction, and execution quality metrics publicly.",
            "problem": "No transparency into solver performance — users can't choose based on execution quality.",
            "solution": "Public leaderboard with fill rate, price improvement, latency, and MEV metrics per solver.",
            "business_model": "Free leaderboard, premium API for institutional flow routing ($199/mo).",
            "effort": "2-3 weeks",
        },
        {
            "title": "Cross-Chain Intent Router",
            "description": "Submit trade intents that can be filled from any chain — solvers bridge and swap atomically.",
            "problem": "Cross-chain swaps require multiple steps, bridges, and trust assumptions.",
            "solution": "Single intent interface where solvers handle bridging, letting users swap Solana tokens for any-chain assets.",
            "business_model": "Bridge fee revenue share with solvers (0.05% of volume).",
            "effort": "6-8 weeks",
        },
    ],
    "PayFi & Payments": [
        {
            "title": "Merchant SDK",
            "description": "Drop-in React component for accepting USDC/SOL payments with instant settlement.",
            "problem": "Merchants want crypto payments but Stripe-like simplicity doesn't exist for Solana.",
            "solution": "npm package with <PayButton /> component — handles wallet detection, tx construction, and confirmation.",
            "business_model": "0.5% transaction fee (vs 2.9% Stripe), volume discounts for large merchants.",
            "effort": "2-3 weeks",
        },
        {
            "title": "Streaming Payments",
            "description": "Payroll and subscription platform using token streaming on Solana.",
            "problem": "Traditional payroll and subscriptions batch payments monthly — misaligned with real-time work.",
            "solution": "Token streaming platform where employees/contractors see earnings accrue by the second.",
            "business_model": "SaaS for employers ($5/employee/mo), free for recipients.",
            "effort": "3-4 weeks",
        },
        {
            "title": "Payment Link Generator",
            "description": "Create shareable payment links with custom amounts, memos, and multi-token support.",
            "problem": "Freelancers and small businesses need simple invoicing without complex integrations.",
            "solution": "Web app to generate payment links — recipient clicks, connects wallet, pays in any SPL token.",
            "business_model": "Free for basic links, $9/mo for custom branding and payment tracking.",
            "effort": "1-2 weeks",
        },
    ],
    "DEX & Aggregation": [
        {
            "title": "DEX Analytics Platform",
            "description": "Real-time analytics for Solana DEX volume, liquidity depth, and price impact across all venues.",
            "problem": "Traders can't compare execution quality across Jupiter, Orca, Raydium, Phoenix in real time.",
            "solution": "Dashboard with live order books, volume charts, price impact simulators, and venue comparison.",
            "business_model": "Free tier with ads, pro tier $29/mo with API access and alerts.",
            "effort": "3-4 weeks",
        },
        {
            "title": "Smart Order Router SDK",
            "description": "Open-source SDK for routing orders across Solana DEXs — build your own Jupiter.",
            "problem": "Projects building trading features must integrate each DEX individually or depend on Jupiter.",
            "solution": "Modular TypeScript SDK with pluggable venue adapters, split routing, and MEV protection.",
            "business_model": "Open-source SDK, paid hosted routing API ($0.001/route) for production use.",
            "effort": "4-6 weeks",
        },
        {
            "title": "LP Position Manager",
            "description": "Manage concentrated liquidity positions across Orca, Raydium, and Meteora from one interface.",
            "problem": "LPs must monitor and rebalance positions across multiple DEXs with different UIs and ranges.",
            "solution": "Unified LP dashboard with auto-rebalancing, impermanent loss tracking, and yield comparison.",
            "business_model": "Performance fee — 5% of LP yield, with a free tier for small positions.",
            "effort": "4-5 weeks",
        },
    ],
    "Perpetuals & Derivatives": [
        {
            "title": "Perp Aggregator",
            "description": "Compare and route perp trades across Drift, Zeta, and others for best funding rates.",
            "problem": "Funding rates differ across perp venues — traders miss arbitrage and overpay for positions.",
            "solution": "Aggregator that shows funding rates across venues and routes to the best one, with position management.",
            "business_model": "Referral fees from venues (10-20% of protocol fees on routed volume).",
            "effort": "3-4 weeks",
        },
        {
            "title": "Structured Products Builder",
            "description": "Create and deploy options vaults and structured products on Solana perp protocols.",
            "problem": "DeFi users want yield but covered calls and straddles require manual management.",
            "solution": "Vault builder where strategists create structured products and users deposit — auto-managed.",
            "business_model": "Management fee (2%) + performance fee (20% of profit above hurdle).",
            "effort": "6-8 weeks",
        },
        {
            "title": "Risk Dashboard for Perps",
            "description": "Track liquidation risk, funding costs, and PnL across all Solana perp positions.",
            "problem": "Traders with positions on multiple venues can't see aggregate risk or total exposure.",
            "solution": "Portfolio-level risk dashboard with liquidation alerts, margin tracking, and scenario analysis.",
            "business_model": "Freemium — free for 1 venue, $19/mo for multi-venue with alerts.",
            "effort": "2-3 weeks",
        },
    ],
    "On-Chain Orderbooks": [
        {
            "title": "Orderbook Visualizer",
            "description": "Real-time depth chart and order flow visualization for Phoenix and other Solana CLOBs.",
            "problem": "On-chain orderbooks exist but lack the visualization tools professional traders expect.",
            "solution": "Web app with real-time depth charts, trade tape, and order flow analytics for Solana CLOBs.",
            "business_model": "Free basic view, $29/mo for advanced analytics and historical data.",
            "effort": "2-3 weeks",
        },
        {
            "title": "Market Making Bot Framework",
            "description": "Open-source framework for running market-making strategies on Solana orderbook DEXs.",
            "problem": "Market making on Solana CLOBs requires custom infrastructure — high barrier to entry.",
            "solution": "Configurable bot framework with strategy templates, risk limits, and performance monitoring.",
            "business_model": "Open-source framework, paid cloud hosting ($99/mo) with monitoring.",
            "effort": "4-6 weeks",
        },
        {
            "title": "CLOB-AMM Hybrid Router",
            "description": "Smart router that splits orders between orderbooks and AMMs for optimal execution.",
            "problem": "Liquidity is fragmented between CLOBs (Phoenix) and AMMs (Orca) — single-venue trades get worse prices.",
            "solution": "Router that simulates execution across both venue types and optimally splits orders.",
            "business_model": "Routing fee (0.01% of volume routed through hybrid path).",
            "effort": "3-4 weeks",
        },
    ],
}

# Default generic ideas when no specific category matches
DEFAULT_IDEAS = [
    {
        "title": "Ecosystem Dashboard",
        "description": "Real-time monitoring tool tracking key metrics for this emerging Solana narrative.",
        "problem": "No unified view of activity and growth metrics for this emerging trend.",
        "solution": "Live dashboard with charts, alerts, and leaderboards tracking the narrative's key metrics.",
        "business_model": "Freemium SaaS — free public view, premium API and alerts ($19/mo).",
        "effort": "2-3 weeks",
    },
    {
        "title": "Developer Toolkit",
        "description": "SDK and CLI tools to help developers build on this narrative quickly.",
        "problem": "Developers entering this space must piece together docs, examples, and boilerplate from scratch.",
        "solution": "npm/cargo package with templates, utility functions, and a CLI for scaffolding projects.",
        "business_model": "Open-source toolkit, paid managed hosting and template marketplace.",
        "effort": "3-4 weeks",
    },
    {
        "title": "Analytics API",
        "description": "Public API providing historical and real-time data for researchers and builders.",
        "problem": "No programmatic access to structured data about this trend — everyone scrapes their own.",
        "solution": "REST + WebSocket API with historical data, real-time events, and aggregated metrics.",
        "business_model": "Free tier (100 req/day), developer tier $29/mo, enterprise custom pricing.",
        "effort": "3-4 weeks",
    },
]

LABEL_PROMPT = """You are an expert Solana ecosystem analyst. Given these signal descriptions from a cluster of related signals, generate:
1. A concise narrative label (3-6 words)
2. A 2-3 sentence summary of the narrative
3. A "why now" explanation (1-2 sentences)
4. A comparable historical precedent (1 sentence)

Signals:
{signals}

Respond in JSON: {{"label": "...", "summary": "...", "why_now": "...", "comparable_precedent": "..."}}"""

IDEAS_PROMPT = """You are a Solana hackathon mentor. Given this detected narrative, suggest 3 build ideas.

Narrative: {label}
Summary: {summary}

Respond as JSON array: [{{"title": "...", "description": "..."}}]"""


def generate_label(signals: list[dict]) -> str:
    """Generate a label for a narrative cluster using keyword matching."""
    combined = " ".join(s.get("description", "").lower() for s in signals)
    best_label = "Emerging Solana Trend"
    best_score = 0
    for keywords, label in LABEL_KEYWORDS:
        score = sum(1 for kw in keywords if kw in combined)
        if score > best_score:
            best_score = score
            best_label = label
    return best_label


def generate_summary(label: str, signals: list[dict]) -> str:
    """Generate a summary for the narrative."""
    domains = set(s.get("domain", "") for s in signals)
    authors = [s.get("author", "") for s in signals if s.get("author")][:5]
    domain_str = ", ".join(sorted(domains))
    n = len(signals)
    return (
        f"{label} is an emerging narrative detected across {domain_str} domains "
        f"based on {n} signals. Key voices include {', '.join(authors[:3])}."
    )


def generate_why_now(label: str, signals: list[dict]) -> str:
    """Generate a why-now explanation."""
    recent = sorted(signals, key=lambda s: s.get("timestamp", ""), reverse=True)
    latest = recent[0] if recent else {}
    return (
        f"Recent activity surge detected — latest signal: "
        f"\"{latest.get('description', '')[:120]}…\" "
        f"({latest.get('domain', 'unknown')} domain)"
    )


def get_build_ideas(label: str) -> list[dict]:
    """Return build ideas — try GPT later, fallback to curated dict."""
    for key, ideas in FALLBACK_BUILD_IDEAS.items():
        if key.lower() in label.lower() or label.lower() in key.lower():
            return ideas
    # Fuzzy match
    label_lower = label.lower()
    for key, ideas in FALLBACK_BUILD_IDEAS.items():
        words = set(key.lower().split())
        if len(words & set(label_lower.split())) >= 2:
            return ideas
    return DEFAULT_IDEAS


async def generate_build_ideas(narratives: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Enrich narratives with labels, summaries, why_now, and build ideas."""
    logger.info(f"💡 Generating ideas for {len(narratives)} narratives...")

    for narrative in narratives:
        signals = narrative.get("signals", [])

        # Label
        if not narrative.get("label") or narrative["label"] == "Emerging Solana Trend":
            narrative["label"] = generate_label(signals)

        # Summary
        narrative["summary"] = generate_summary(narrative["label"], signals)

        # Why now
        narrative["why_now"] = generate_why_now(narrative["label"], signals)

        # Comparable precedent
        narrative["comparable_precedent"] = (
            "Similar to early DeFi Summer (2020) momentum patterns on Ethereum — "
            "cross-domain activity acceleration preceding mainstream breakout."
        )

        # Entities
        entities: dict[str, list[str]] = {"programs": [], "repos": [], "kols": []}
        for s in signals:
            meta = s.get("metadata", {})
            if meta.get("program_name"):
                entities["programs"].append(meta["program_name"])
            if meta.get("full_name"):
                entities["repos"].append(meta["full_name"])
            if meta.get("username"):
                entities["kols"].append(f"@{meta['username']}")
        # Deduplicate
        for k in entities:
            entities[k] = list(dict.fromkeys(entities[k]))[:10]
        narrative["entities"] = entities

        # Build ideas
        narrative["build_ideas"] = get_build_ideas(narrative["label"])

        # Evidence — top signal snippets per domain
        evidence_list = []
        by_domain: dict[str, list[dict]] = {}
        for s in signals:
            dom = s.get("domain", "unknown")
            by_domain.setdefault(dom, []).append(s)
        # Take balanced evidence across domains
        for dom_signals in by_domain.values():
            for s in dom_signals[:5]:
                evidence_list.append({
                    "signal_id": s.get("id", ""),
                    "domain": s.get("domain", ""),
                    "description": s.get("description", "")[:200],
                    "url": s.get("url", ""),
                })
        narrative["evidence"] = evidence_list[:10]

    # Try GPT-4 enrichment if available
    if HAS_OPENAI and settings.openai_api_key:
        try:
            client = AsyncOpenAI(api_key=settings.openai_api_key)
            for narrative in narratives[:5]:  # limit to top 5 to save tokens
                signals = narrative.get("signals", [])
                signal_text = "\n".join(
                    f"- [{s.get('domain')}] {s.get('description', '')[:150]}"
                    for s in signals[:10]
                )
                # Get better label + summary from GPT
                import json
                resp = await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": LABEL_PROMPT.format(signals=signal_text)}],
                    temperature=0.4,
                    max_tokens=300,
                )
                raw = resp.choices[0].message.content or ""
                # Try to parse JSON from response
                raw = raw.strip()
                if raw.startswith("```"):
                    raw = re.sub(r"```\w*\n?", "", raw).strip()
                data = json.loads(raw)
                narrative["label"] = data.get("label", narrative["label"])
                narrative["summary"] = data.get("summary", narrative["summary"])
                narrative["why_now"] = data.get("why_now", narrative["why_now"])
                narrative["comparable_precedent"] = data.get("comparable_precedent", narrative["comparable_precedent"])
        except Exception as e:
            logger.warning(f"GPT enrichment failed ({e}), keeping heuristic labels")

    logger.info("✅ Narrative enrichment complete")
    return narratives
