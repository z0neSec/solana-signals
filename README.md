# Pulse — Solana Narrative Detection

> Detecting emerging narratives on Solana before they become obvious.

## What This Does

Pulse monitors onchain activity, developer momentum, and social signals across the Solana ecosystem to surface emerging narratives **fortnightly**. Each detected narrative includes:

- **Confidence Score** — Multi-factor certainty rating (domain coverage, temporal consistency, source credibility, novelty)
- **Evidence Chain** — Verifiable data points across onchain, GitHub, and social domains
- **Build Ideas** — 3-5 actionable product opportunities with problem/solution/effort/business model

The tool prioritises **novelty** (new trends over established ones), **signal quality** (cross-domain validation over volume), and **explainability** (every score is decomposed).

---

## Current Detected Narratives (Jan 31 – Feb 14, 2026)

| # | Narrative | Status | Confidence | Signals | Domains | Build Ideas |
|---|-----------|--------|------------|---------|---------|-------------|
| 1 | AI Agents on Solana | 📈 ACCELERATING | 75% | 9 | onchain, github, social | 4 |
| 2 | Compressed NFTs / State Compression | 🆕 NEW | 67% | 12 | onchain, github, social | 3 |
| 3 | DePIN Infrastructure | 🆕 NEW | 67% | 12 | onchain, github, social | 3 |
| 4 | DEX & Aggregation | 📈 ACCELERATING | 64% | 14 | onchain, github | 3 |
| 5 | Solana Blinks & Actions | 📈 ACCELERATING | 60% | 10 | github, social | 3 |

> *Narratives are re-detected every pipeline run from live data. The table above reflects the most recent run.*

### Narrative 1: AI Agents on Solana (75%, ACCELERATING)

**Summary**: Multiple AI agent frameworks gaining GitHub traction. On-chain activity from agent-related programs. KOL discussions around autonomous wallet operations intensifying.

**Why Now**: Solana's low fees make frequent agent transactions economically viable. Recent LLM function-calling advances enable reliable transaction construction. Growing demand for automated DeFi strategies.

**Build Ideas**:
1. **Agent Launchpad** — No-code platform to deploy AI agents that execute on-chain actions. *Freemium SaaS — $49/mo for teams. 4-6 weeks.*
2. **Agent Analytics Dashboard** — Monitor autonomous agent wallet activity, PnL, and strategy performance. *SaaS $29/mo per agent. 2-3 weeks.*
3. **Multi-Agent Orchestrator** — Framework for composing specialized agents that collaborate on complex DeFi strategies. *OSS + managed cloud. 6-8 weeks.*
4. **Scoped Wallet Delegation** — On-chain program for granular permission delegation with spend limits and expiry. *Protocol fee 0.01%. 3-4 weeks.*

### Narrative 2: Compressed NFTs / State Compression (67%, NEW)

**Summary**: State Compression and Bubblegum programs showing onchain activity. GitHub repos exploring cNFT tooling, minting infrastructure, and compression utilities trending across ecosystem.

**Why Now**: Compressed NFTs reduce minting costs 1000×, enabling mass distribution use cases (loyalty, tickets, credentials). DRiP, Dialect, and others driving adoption.

**Build Ideas**:
1. **cNFT Minting API** — REST API for minting millions of compressed NFTs without Solana expertise. *Usage-based pricing per mint. 3-4 weeks.*
2. **cNFT Analytics Explorer** — Track compressed NFT collections, ownership, transfers, and Merkle tree utilisation. *Freemium + $19/mo pro. 2-3 weeks.*
3. **Loyalty Program SDK** — Full-stack SDK for brands to issue, distribute, and redeem compressed NFT loyalty passes. *B2B SaaS $99/mo. 4-5 weeks.*

### Narrative 3: DePIN Infrastructure (67%, NEW)

**Summary**: DePIN-related GitHub repos and social discussions accelerating. Programs tied to physical infrastructure networks showing activity on-chain.

**Why Now**: Helium's migration to Solana proved the model. Hivemapper, Render, and new DePIN projects launching. Real-world infrastructure + crypto incentives gaining mainstream credibility.

**Build Ideas**:
1. **DePIN Node Dashboard** — Unified monitoring for node operators across Helium, Hivemapper, Render with earnings tracking. *Freemium + $19/mo pro. 3-4 weeks.*
2. **DePIN Coverage Mapper** — Visualise network coverage gaps and incentivise deployment in underserved areas. *B2B licensing to DePIN protocols. 4-5 weeks.*
3. **DePIN Yield Aggregator** — Compare and optimise hardware staking across DePIN networks. *1% management fee. 3-4 weeks.*

### Narrative 4: DEX & Aggregation (64%, ACCELERATING)

**Summary**: Jupiter, Orca Whirlpool, and Phoenix DEX showing elevated on-chain activity with high unique wallet counts. GitHub trending repos include new DEX tooling and aggregation SDKs.

**Why Now**: Record Solana DEX volume driven by meme coin activity and improved aggregator routing. Phoenix on-chain orderbook gaining traction as a CLOB alternative to AMMs.

**Build Ideas**:
1. **DEX Analytics Platform** — Real-time volume, liquidity depth, and price impact comparison across all Solana venues. *Freemium SaaS, $29/mo pro tier. 3-4 weeks.*
2. **Smart Order Router SDK** — Open-source SDK for routing orders across Solana DEXs with MEV protection. *OSS + paid hosted API. 4-6 weeks.*
3. **LP Position Manager** — Unified interface to manage concentrated liquidity positions across Orca, Raydium, and Meteora with auto-rebalancing. *5% performance fee. 4-5 weeks.*

### Narrative 5: Solana Blinks & Actions (60%, ACCELERATING)

**Summary**: Blinks (blockchain links) and Actions framework gaining developer mindshare on GitHub with social amplification from KOLs. New use cases for shareable on-chain actions emerging.

**Why Now**: Blinks make Solana transactions embeddable anywhere — tweets, websites, Discord. Low friction onboarding + viral distribution = network effect potential.

**Build Ideas**:
1. **Blink Builder Studio** — Visual editor to create, customize, and deploy Blinks without code. *Freemium + $19/mo for custom branding. 2-3 weeks.*
2. **Blink Analytics** — Track click-through, conversion, and transaction completion rates for deployed Blinks. *SaaS $29/mo. 2-3 weeks.*
3. **Blink Commerce SDK** — E-commerce toolkit for one-click Solana payments via embeddable Blinks. *0.5% transaction fee. 3-4 weeks.*

---

## Data Sources

| Domain | Source | What We Collect | Update Frequency |
|--------|--------|-----------------|------------------|
| **Onchain** | [Helius API](https://helius.dev) | Program activity for 10 tracked programs (Jupiter, Orca, Magic Eden, Metaplex, Bubblegum, State Compression, Phoenix, Drift, Marinade, Jito), network health, priority fees | Every pipeline run |
| **GitHub** | [GitHub REST API](https://docs.github.com/en/rest) | Trending Solana repos (stars, forks, recent pushes), notable commits across ecosystem projects | Every pipeline run |
| **Social** | [Twitter API v2](https://developer.twitter.com) | KOL tweets (Toly, Mert, Akshay, etc.), ecosystem topic searches; curated fallback when rate-limited | Every pipeline run |

### Tracked Programs (Onchain)

| Program | Address |
|---------|---------|
| Jupiter Aggregator | `JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4` |
| Orca Whirlpool | `whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc` |
| Magic Eden | `M2mx93ekt1fmXSVkTrUL9xVFHkmME8HTUi5Cyc5aF7K` |
| Metaplex Token Metadata | `metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s` |
| Bubblegum (cNFTs) | `BGUMAp9Gq7iTEuizy4pqaxsTyUCBK68MDfK752saRPUY` |
| State Compression | `cmtDvXumGCrqC1Age74AVPhSRVXJMd8PJS91L8KbNCK` |
| Phoenix DEX | `PhoeNiXZ8ByJGLkxNfZRnkUfjvmuYqLR89jjFHGqdXY` |
| Drift Protocol | `dRiftyHA39MWEi3m9aunc5MzRF1JYuBsbn6VPcn33UH` |
| Marinade Finance | `MarBmsSgKXdrN1egZf5sqe1TMai9K1rChYNDJgjq7aD` |
| Jito Staking | `Jito4APyf642JPZPx3hGc6WWJ8zPKtRbRs4P815Awbb` |

### Tracked KOLs (Social)

Toly (@aeyakovenko), Raj Gokal (@rajgokal), Mert (@0xMert_), Akshay (@akshay_bd), Armani Ferrante (@armaniferrante), Chase Barker (@therealchaseeb), Jupiter (@JupiterExchange), Helius (@helius_labs), and more.

---

## How Signals Are Detected & Ranked

### Signal Detection Pipeline

```
Data Ingestion → Normalization → Embedding → Clustering → Scoring → Enrichment → Output
```

#### 1. Data Ingestion
- **Onchain**: Enhanced transaction data from Helius for 10 tracked programs — transaction count, unique wallets, network health metrics
- **GitHub**: Repository search with 10 Solana-specific queries (AI agent, blinks, DePIN, token extensions, etc.), recent commits from ecosystem projects
- **Social**: Twitter API v2 search for KOL discussions and ecosystem topics; curated fallback signals when rate-limited

#### 2. Embedding
- All signals converted to descriptive text
- Embedded using OpenAI `text-embedding-3-small` (1536 dimensions)
- Fallback: deterministic hash-based vectors (SHA256-seeded, reproducible) when API is unavailable
- Vectors stored in Pinecone for similarity search

#### 3. Narrative Clustering
- **Primary**: HDBSCAN (density-based, handles noise naturally)
- **Fallback**: KMeans when HDBSCAN is not available
- Cross-domain validation: narratives must include signals from multiple domains
- Post-processing: duplicate labels are merged, combining signal sets

#### 4. Scoring & Ranking

```
narrative_score = (
    onchain_score × 0.40 +     # Can't fake blockchain activity
    github_score  × 0.35 +     # Commits require real effort
    social_score  × 0.25       # Easier to manipulate, lower weight
) × freshness_weight × novelty_bonus
```

| Confidence Factor | Weight | Description |
|-------------------|--------|-------------|
| Domain Coverage | 25% | How many data domains confirm the signal |
| Temporal Consistency | 25% | Sustained over days, not a single spike |
| Source Credibility | 20% | KOL tier, program verification status |
| Signal Volume | 15% | Raw count of related signals |
| Novelty | 15% | First-time appearance bonus (1.5× multiplier) |

#### 5. Enrichment
- Narrative labels generated via keyword classification (16 categories) with GPT-4o-mini upgrade when available
- Build ideas drawn from curated database of 30+ ideas across 11 categories, each with problem/solution/business model/effort
- Evidence chains compiled from top signals per domain

### Why This Finds Signals Early

1. **Novelty Over Popularity** — Explicitly scores "never seen before" higher than "talked about a lot"
2. **Cross-Domain Correlation** — Single-source spikes = noise; multi-source convergence = signal
3. **Acceleration Detection** — Measures rate-of-change, not absolute values
4. **Weighted Domain Trust** — Onchain (40%) > GitHub (35%) > Social (25%) reflects manipulation difficulty

---

## Running Locally

### Prerequisites
- Python 3.11+
- Node.js 18+
- API keys (see below)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/solana-signals
cd solana-signals

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # Fill in your API keys
uvicorn main:app --port 8000 # Starts on http://localhost:8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev -- -p 3001       # Starts on http://localhost:3001
```

The pipeline runs automatically on startup — signals are ingested, embedded, clustered, scored, and enriched. Results are available via the dashboard within ~2 minutes.

### Environment Variables

Create `backend/.env` from `.env.example`:

```bash
# Required
OPENAI_API_KEY=sk-...           # Embeddings + GPT enrichment (falls back gracefully)
HELIUS_API_KEY=...              # Onchain data from Helius
TWITTER_BEARER_TOKEN=...       # Social signals (falls back to curated signals)

# Database (Supabase free tier)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...

# Vector DB (Pinecone free tier)
PINECONE_API_KEY=...
PINECONE_INDEX_NAME=solana-signals

# Optional
GITHUB_TOKEN=ghp_...           # Higher rate limits for GitHub API
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/dashboard` | GET | Dashboard with all narratives + summary stats |
| `/api/narratives` | GET | List narratives (filterable by status, confidence) |
| `/api/narratives/{id}` | GET | Narrative detail with evidence, entities, build ideas |
| `/api/signals` | GET | Signal stream (filterable by domain) |
| `/api/methodology` | GET | Methodology documentation |
| `/api/export/markdown` | GET | Export narratives as Markdown report |
| `/api/pipeline/trigger` | POST | Manually trigger full pipeline |

---

## Architecture

```
solana-signals/
├── backend/
│   ├── main.py                    # FastAPI app + startup pipeline
│   ├── config.py                  # Settings, domain weights, tracked KOLs
│   ├── api/
│   │   ├── routes.py              # API endpoints
│   │   └── models.py              # Pydantic response models
│   ├── ingestors/
│   │   ├── onchain.py             # Helius API — program activity, network health
│   │   ├── github.py              # GitHub API — trending repos, commits
│   │   ├── social.py              # Twitter API + curated fallback
│   │   └── coordinator.py         # Runs all ingestors, handles storage
│   ├── processing/
│   │   ├── pipeline.py            # Full pipeline orchestration + in-memory cache
│   │   ├── embeddings.py          # OpenAI embeddings + Pinecone storage
│   │   ├── clustering.py          # HDBSCAN / KMeans narrative detection
│   │   ├── scoring.py             # Multi-factor confidence scoring
│   │   └── ideas.py               # Label generation + build ideas (30+ curated)
│   ├── db/
│   │   ├── supabase.py            # Supabase CRUD repositories
│   │   └── schema.sql             # Database schema + RLS policies
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx               # Dashboard — metrics, top narratives, activity
│   │   ├── narratives/page.tsx    # All narratives — filter, search, sort
│   │   ├── narratives/[id]/       # Narrative detail — evidence, scores, ideas
│   │   ├── signals/page.tsx       # Signal stream table
│   │   ├── report/page.tsx        # Print-ready export report
│   │   ├── methodology/page.tsx   # How it works
│   │   └── layout.tsx             # App shell + navigation
│   ├── components/
│   │   ├── DataDisplay.tsx        # MetricCard, NarrativeCard, ConfidenceBar, etc.
│   │   ├── Navigation.tsx         # Top nav with theme toggle
│   │   ├── Skeleton.tsx           # Loading skeletons
│   │   └── States.tsx             # Empty + error states
│   ├── lib/api.ts                 # API client + TypeScript types
│   └── package.json
├── README.md
├── LICENSE
└── docker-compose.yml
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, FastAPI, uvicorn |
| Frontend | Next.js 14 (App Router), React, TypeScript, Tailwind CSS |
| Database | Supabase (PostgreSQL + pgvector) |
| Vector Store | Pinecone (1536-dim cosine similarity) |
| Embeddings | OpenAI text-embedding-3-small |
| LLM | GPT-4o-mini (narrative enrichment) |
| Onchain Data | Helius API (enhanced transactions, RPC) |
| Social Data | Twitter API v2 |
| Dev Activity | GitHub REST API |

---

## Evaluation Criteria Alignment

| Criteria | How We Address It |
|----------|------------------|
| **Quality of signal detection** | Multi-domain fusion (onchain 40% + GitHub 35% + social 25%), bot/hype filtering, cross-domain validation, acceleration thresholds |
| **Originality of narratives** | Novelty scoring (1.5× bonus for first-detections), specific labels (not generic "DeFi"), keyword classification across 16 categories |
| **Practicality of build ideas** | Each idea includes problem/solution/business model/effort estimate; 30+ curated ideas across 11 categories |
| **Clarity** | Evidence chains with source links, decomposed confidence scores, methodology transparency, print-ready reports |

---

Built for the **Solana Ecosystem Narrative Detection Bounty**, February 2026.
