"""Global state management for CryptoAnalyst LangGraph workflows."""

from typing import Any, Dict, List, TypedDict


class GlobalState(TypedDict):
    ticker: str
    price_history: List[Dict]
    technical_indicators: Dict[str, float]
    news_articles: List[Dict]
    sentiment_scores: Dict[str, float]
    risk_profile: Dict[str, Any]
    user_feedback: Dict[str, Any]
    messages: List[dict]
