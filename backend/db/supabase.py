"""
Supabase client for database operations.
"""
import os
from supabase import create_client, Client
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load .env file from the backend directory
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

_client: Optional[Client] = None


def get_client() -> Client:
    """Get or create Supabase client."""
    global _client
    if _client is None:
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")
        _client = create_client(supabase_url, supabase_key)
    return _client


class SignalRepository:
    """Repository for signal operations."""
    
    @staticmethod
    def create(signal: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new signal."""
        client = get_client()
        result = client.table("signals").insert(signal).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def create_many(signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create multiple signals."""
        client = get_client()
        result = client.table("signals").insert(signals).execute()
        return result.data
    
    @staticmethod
    def get_by_id(signal_id: str) -> Optional[Dict[str, Any]]:
        """Get signal by ID."""
        client = get_client()
        result = client.table("signals").select("*").eq("id", signal_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_by_narrative(narrative_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get signals for a narrative."""
        client = get_client()
        result = (
            client.table("signals")
            .select("*")
            .eq("narrative_id", narrative_id)
            .order("timestamp", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data
    
    @staticmethod
    def get_recent(days: int = 14, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent signals."""
        client = get_client()
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        result = (
            client.table("signals")
            .select("*, narratives(label)")
            .gte("timestamp", cutoff)
            .order("timestamp", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data
    
    @staticmethod
    def get_unprocessed(limit: int = 100) -> List[Dict[str, Any]]:
        """Get unprocessed signals."""
        client = get_client()
        result = (
            client.table("signals")
            .select("*")
            .eq("processed", False)
            .order("timestamp", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data
    
    @staticmethod
    def update(signal_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a signal."""
        client = get_client()
        result = client.table("signals").update(updates).eq("id", signal_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def count_by_domain(days: int = 14) -> Dict[str, int]:
        """Count signals by domain."""
        client = get_client()
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        result = (
            client.table("signals")
            .select("domain")
            .gte("timestamp", cutoff)
            .execute()
        )
        counts = {}
        for signal in result.data:
            domain = signal["domain"]
            counts[domain] = counts.get(domain, 0) + 1
        return counts


class NarrativeRepository:
    """Repository for narrative operations."""
    
    @staticmethod
    def create(narrative: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new narrative."""
        client = get_client()
        result = client.table("narratives").insert(narrative).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_by_id(narrative_id: str) -> Optional[Dict[str, Any]]:
        """Get narrative by ID."""
        client = get_client()
        result = client.table("narratives").select("*").eq("id", narrative_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_all(
        status: Optional[str] = None,
        min_confidence: Optional[float] = None,
        limit: int = 10,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get all narratives with optional filtering."""
        client = get_client()
        query = client.table("narratives").select("*")
        
        if status:
            query = query.eq("status", status.upper())
        
        if min_confidence is not None:
            query = query.gte("confidence", min_confidence)
        
        result = (
            query
            .order("rank", desc=False)
            .order("confidence", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )
        return result.data
    
    @staticmethod
    def get_current_fortnight(limit: int = 10) -> List[Dict[str, Any]]:
        """Get narratives from current fortnight."""
        client = get_client()
        cutoff = (datetime.now() - timedelta(days=14)).date().isoformat()
        result = (
            client.table("narratives")
            .select("*")
            .gte("fortnight_start", cutoff)
            .order("rank", desc=False)
            .limit(limit)
            .execute()
        )
        return result.data
    
    @staticmethod
    def get_with_signals(narrative_id: str) -> Optional[Dict[str, Any]]:
        """Get narrative with its signals."""
        client = get_client()
        
        # Get narrative
        narrative = NarrativeRepository.get_by_id(narrative_id)
        if not narrative:
            return None
        
        # Get signals
        signals = SignalRepository.get_by_narrative(narrative_id)
        narrative["signals"] = signals
        
        return narrative
    
    @staticmethod
    def update(narrative_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a narrative."""
        client = get_client()
        result = client.table("narratives").update(updates).eq("id", narrative_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def count() -> int:
        """Count total narratives."""
        client = get_client()
        result = client.table("narratives").select("id", count="exact").execute()
        return result.count or 0
    
    @staticmethod
    def count_by_status() -> Dict[str, int]:
        """Count narratives by status."""
        client = get_client()
        result = client.table("narratives").select("status").execute()
        counts = {}
        for narrative in result.data:
            status = narrative["status"]
            counts[status] = counts.get(status, 0) + 1
        return counts


class DashboardRepository:
    """Repository for dashboard data."""
    
    @staticmethod
    def get_summary() -> Dict[str, Any]:
        """Get dashboard summary."""
        client = get_client()
        
        # Get narrative counts
        narrative_counts = NarrativeRepository.count_by_status()
        
        # Get signal counts by domain
        signal_counts = SignalRepository.count_by_domain()
        
        # Get total signals
        total_signals = sum(signal_counts.values())
        
        # Get top narratives
        top_narratives = NarrativeRepository.get_current_fortnight(limit=5)
        
        return {
            "total_narratives": sum(narrative_counts.values()),
            "new_narratives": narrative_counts.get("NEW", 0),
            "accelerating_narratives": narrative_counts.get("ACCELERATING", 0),
            "stable_narratives": narrative_counts.get("STABLE", 0),
            "total_signals": total_signals,
            "signals_by_domain": signal_counts,
            "data_sources": len(signal_counts),
            "top_narratives": top_narratives
        }


def init_db():
    """Initialize database connection and verify schema."""
    try:
        client = get_client()
        # Test connection with a simple query
        client.table("fortnights").select("id").limit(1).execute()
        print("✓ Database connection successful")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False
