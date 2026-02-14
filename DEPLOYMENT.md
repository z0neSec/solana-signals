# Deployment Guide

## Quick Start (Local Development)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python main.py
```

Backend runs at: http://localhost:8000

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:3000

---

## Production Deployment

### Option 1: Vercel + Railway (Recommended for Hackathon)

**Frontend (Vercel)**

1. Push code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your repository
4. Set root directory to `frontend`
5. Add environment variable:
   - `API_URL` = Your Railway backend URL

**Backend (Railway)**

1. Go to [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Select your repository
4. Set root directory to `backend`
5. Add environment variables from `.env.example`
6. Railway auto-detects Python and deploys

**Cost**: Free tier for both (sufficient for demo)

### Option 2: Docker Compose (Self-Hosted)

```bash
# Set environment variables
cp backend/.env.example .env
# Edit .env with production values

# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Option 3: Fly.io (Full-Stack)

**Backend**

```bash
cd backend
fly launch --name solana-signals-api
fly secrets set OPENAI_API_KEY=sk-...
fly secrets set HELIUS_API_KEY=...
# Set all other secrets
fly deploy
```

**Frontend**

```bash
cd frontend
fly launch --name solana-signals-web
fly secrets set API_URL=https://solana-signals-api.fly.dev
fly deploy
```

---

## Database Setup (Supabase)

1. Create account at [supabase.com](https://supabase.com)
2. Create new project
3. Go to SQL Editor
4. Run the schema from `backend/db/models.py` (SQL_SCHEMA constant)
5. Copy URL and anon key to your `.env`

## Vector Database (Pinecone)

1. Create account at [pinecone.io](https://pinecone.io)
2. Create new index:
   - Name: `solana-signals`
   - Dimensions: 1536
   - Metric: cosine
3. Copy API key and environment to `.env`

---

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | For embeddings and label generation |
| `HELIUS_API_KEY` | Yes | For Solana onchain data |
| `TWITTER_BEARER_TOKEN` | Yes | For social signals |
| `SUPABASE_URL` | Yes | PostgreSQL database |
| `SUPABASE_KEY` | Yes | Database access key |
| `PINECONE_API_KEY` | Yes | Vector database |
| `PINECONE_INDEX_NAME` | No | Defaults to `solana-signals` |
| `GITHUB_TOKEN` | No | Higher rate limits |
| `ENVIRONMENT` | No | `development` or `production` |

---

## Cron Jobs (Data Refresh)

For fortnightly updates, set up a cron job or use Railway's scheduled tasks:

```bash
# Run full pipeline every 14 days
0 0 1,15 * * cd /app && python -c "from main import run_pipeline; import asyncio; asyncio.run(run_pipeline())"
```

Or use GitHub Actions:

```yaml
# .github/workflows/refresh.yml
name: Refresh Data
on:
  schedule:
    - cron: '0 0 1,15 * *'
  workflow_dispatch:

jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: |
          cd backend
          pip install -r requirements.txt
          python -c "from main import run_pipeline; import asyncio; asyncio.run(run_pipeline())"
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          # ... other secrets
```

---

## Monitoring

- **Uptime**: Use [uptimerobot.com](https://uptimerobot.com) (free)
- **Logs**: Railway/Vercel built-in
- **Errors**: Consider [sentry.io](https://sentry.io) (free tier)

---

## Cost Estimate

| Service | Free Tier | Paid Estimate |
|---------|-----------|---------------|
| Vercel | 100GB bandwidth | $0 |
| Railway | $5 credit/month | $5/month |
| Supabase | 500MB database | $0 |
| Pinecone | 1 index free | $0 |
| OpenAI | Pay-per-use | ~$2/month |
| Helius | 100k credits/day | $0 |
| Twitter | Basic tier | $100/month (or use free tier limits) |

**Hackathon Total**: $0-5/month with free tiers
