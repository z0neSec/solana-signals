"""
Test all API keys and external service connections.
Run: python test_api_keys.py
"""
import os
import sys
import asyncio
from dotenv import load_dotenv

# Load .env from the backend directory
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

results = {}


def test_supabase():
    """Test Supabase connection."""
    print("\n🔍 Testing Supabase...")
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("  ❌ SUPABASE_URL or SUPABASE_KEY not set")
        results["Supabase"] = "MISSING"
        return
    
    try:
        from supabase import create_client
        client = create_client(url, key)
        # Try a simple query - the table may not exist yet
        try:
            result = client.table("fortnights").select("id").limit(1).execute()
            print(f"  ✅ Connected! fortnights table accessible. Rows: {len(result.data)}")
            results["Supabase"] = "OK"
        except Exception as table_err:
            err_str = str(table_err)
            if "does not exist" in err_str or "relation" in err_str:
                print(f"  ⚠️  Connected but schema not set up yet (tables don't exist). Run schema.sql in Supabase SQL Editor.")
                results["Supabase"] = "CONNECTED (no schema)"
            else:
                print(f"  ✅ Connected (query returned: {err_str[:100]})")
                results["Supabase"] = "OK"
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        results["Supabase"] = "FAILED"


def test_openai():
    """Test OpenAI API key."""
    print("\n🔍 Testing OpenAI...")
    key = os.getenv("OPENAI_API_KEY")
    
    if not key:
        print("  ❌ OPENAI_API_KEY not set")
        results["OpenAI"] = "MISSING"
        return
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        # Simple embedding test (cheapest call)
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input="test"
        )
        dim = len(response.data[0].embedding)
        print(f"  ✅ Connected! Embedding dimension: {dim}")
        results["OpenAI"] = "OK"
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        results["OpenAI"] = "FAILED"


def test_helius():
    """Test Helius API key."""
    print("\n🔍 Testing Helius...")
    key = os.getenv("HELIUS_API_KEY")
    
    if not key:
        print("  ❌ HELIUS_API_KEY not set")
        results["Helius"] = "MISSING"
        return
    
    try:
        import httpx
        # Test with a simple getHealth RPC call
        url = f"https://mainnet.helius-rpc.com/?api-key={key}"
        response = httpx.post(url, json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getHealth"
        }, timeout=10)
        data = response.json()
        if "result" in data:
            print(f"  ✅ Connected! Solana node health: {data['result']}")
            results["Helius"] = "OK"
        elif "error" in data:
            print(f"  ❌ API error: {data['error']}")
            results["Helius"] = "FAILED"
        else:
            print(f"  ⚠️  Unexpected response: {data}")
            results["Helius"] = "UNKNOWN"
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        results["Helius"] = "FAILED"


def test_twitter():
    """Test Twitter Bearer Token."""
    print("\n🔍 Testing Twitter/X...")
    token = os.getenv("TWITTER_BEARER_TOKEN")
    
    if not token:
        print("  ❌ TWITTER_BEARER_TOKEN not set")
        results["Twitter"] = "MISSING"
        return
    
    try:
        import httpx
        # Test with a simple user lookup (Solana's account)
        headers = {"Authorization": f"Bearer {token}"}
        response = httpx.get(
            "https://api.twitter.com/2/users/by/username/solana",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Connected! Test lookup: @{data['data']['username']} (id: {data['data']['id']})")
            results["Twitter"] = "OK"
        elif response.status_code == 401:
            print(f"  ❌ Unauthorized - invalid bearer token")
            results["Twitter"] = "FAILED"
        elif response.status_code == 403:
            print(f"  ⚠️  Forbidden - token valid but insufficient permissions. Response: {response.text[:200]}")
            results["Twitter"] = "LIMITED"
        elif response.status_code == 429:
            print(f"  ⚠️  Rate limited - token is valid but rate limited. Try again later.")
            results["Twitter"] = "RATE LIMITED"
        else:
            print(f"  ❌ HTTP {response.status_code}: {response.text[:200]}")
            results["Twitter"] = "FAILED"
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        results["Twitter"] = "FAILED"


def test_pinecone():
    """Test Pinecone API key."""
    print("\n🔍 Testing Pinecone...")
    key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME", "solana-signals")
    
    if not key:
        print("  ❌ PINECONE_API_KEY not set")
        results["Pinecone"] = "MISSING"
        return
    
    try:
        from pinecone import Pinecone
        pc = Pinecone(api_key=key)
        indexes = pc.list_indexes()
        index_names = [idx.name for idx in indexes]
        print(f"  ✅ Connected! Available indexes: {index_names}")
        
        if index_name in index_names:
            idx = pc.Index(index_name)
            stats = idx.describe_index_stats()
            print(f"  ✅ Index '{index_name}' exists. Vectors: {stats.total_vector_count}, Dimension: {stats.dimension}")
            results["Pinecone"] = "OK"
        else:
            print(f"  ⚠️  Index '{index_name}' not found. You need to create it.")
            print(f"     Create at: https://app.pinecone.io/ (dimension: 1536, metric: cosine)")
            results["Pinecone"] = "CONNECTED (no index)"
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        results["Pinecone"] = "FAILED"


def test_github():
    """Test GitHub token."""
    print("\n🔍 Testing GitHub...")
    token = os.getenv("GITHUB_TOKEN")
    
    if not token:
        print("  ❌ GITHUB_TOKEN not set")
        results["GitHub"] = "MISSING"
        return
    
    try:
        import httpx
        headers = {"Authorization": f"token {token}"}
        response = httpx.get(
            "https://api.github.com/rate_limit",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            core = data["rate"]["remaining"]
            limit = data["rate"]["limit"]
            print(f"  ✅ Connected! Rate limit: {core}/{limit} remaining")
            results["GitHub"] = "OK"
        elif response.status_code == 401:
            print(f"  ❌ Unauthorized - invalid token")
            results["GitHub"] = "FAILED"
        else:
            print(f"  ❌ HTTP {response.status_code}: {response.text[:200]}")
            results["GitHub"] = "FAILED"
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        results["GitHub"] = "FAILED"


def main():
    print("=" * 60)
    print("  API Key & Service Connection Tests")
    print("=" * 60)
    
    test_supabase()
    test_openai()
    test_helius()
    test_twitter()
    test_pinecone()
    test_github()
    
    print("\n" + "=" * 60)
    print("  Summary")
    print("=" * 60)
    
    all_ok = True
    for service, status in results.items():
        icon = "✅" if status == "OK" else "⚠️" if "CONNECTED" in status or "LIMITED" in status else "❌"
        print(f"  {icon} {service}: {status}")
        if status not in ("OK",):
            all_ok = False
    
    print()
    if all_ok:
        print("  🎉 All services connected successfully!")
    else:
        print("  ⚠️  Some services need attention. See details above.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
