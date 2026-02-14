"""
Configuration management for Solana Signal Intelligence.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys (optional for demo mode)
    openai_api_key: Optional[str] = None
    helius_api_key: Optional[str] = None
    twitter_bearer_token: Optional[str] = None
    supabase_url: Optional[str] = None
    supabase_key: Optional[str] = None
    pinecone_api_key: Optional[str] = None
    pinecone_index_name: str = "solana-signals"
    github_token: Optional[str] = None
    
    # App Config
    environment: str = "development"
    log_level: str = "INFO"
    fortnight_lookback_days: int = 14
    
    # Domain Weights for scoring
    onchain_weight: float = 0.40
    github_weight: float = 0.35
    social_weight: float = 0.25
    
    # Thresholds
    min_cluster_size: int = 5
    min_confidence_threshold: float = 0.3
    acceleration_threshold: float = 0.25
    novelty_bonus: float = 1.5
    
    # Rate Limiting
    helius_rps: int = 100
    github_requests_per_hour: int = 5000
    twitter_requests_per_15min: int = 300
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Domain weights as a constant for easy access
DOMAIN_WEIGHTS = {
    "onchain": 0.40,
    "github": 0.35,
    "social": 0.25
}

# KOLs to track (curated list of Solana ecosystem voices)
TRACKED_KOLS = [
    "aeyakovenko",       # Toly
    "0xMert_",           # Mert (Helius)
    "akshay_bd",         # Akshay
    "armaniferrante",    # Armani
    "therealchaseeb",    # Chase
    "heaboringdystophy", # Helius
    "solanafndn",        # Solana Foundation
    "solana",            # Official Solana
    "jupiterexchange",   # Jupiter
    "mariaboringdystophy", # Marinade
    "daboringdystophy",  # Drift
]

# Banned generic labels that we want to avoid
BANNED_LABELS = [
    "DeFi",
    "NFTs", 
    "NFT",
    "Gaming",
    "Infrastructure",
    "Payments",
    "Trading",
    "Tokens",
    "Crypto",
    "Blockchain",
    "Web3",
    "Solana Growth",
    "Ecosystem Growth",
]
