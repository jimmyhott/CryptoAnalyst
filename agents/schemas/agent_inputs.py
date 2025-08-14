"""Input schemas for CryptoAnalyst agents."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AgentInput(BaseModel):
    """Base input schema for all agents."""
    
    session_id: Optional[str] = Field(default=None, description="Session ID for tracking")
    user_id: Optional[str] = Field(default=None, description="User ID")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class CryptoAnalysisInput(AgentInput):
    """Input schema for cryptocurrency analysis."""
    
    symbol: str = Field(..., description="Cryptocurrency symbol (e.g., BTC, ETH)")
    analysis_type: str = Field(
        default="comprehensive",
        description="Type of analysis: technical, fundamental, sentiment, comprehensive"
    )
    timeframe: Optional[str] = Field(default="1d", description="Analysis timeframe")
    include_news: bool = Field(default=True, description="Include news sentiment analysis")
    include_social: bool = Field(default=True, description="Include social media sentiment")


class PortfolioAnalysisInput(AgentInput):
    """Input schema for portfolio analysis."""
    
    portfolio_data: Dict[str, Any] = Field(..., description="Portfolio holdings and data")
    analysis_type: str = Field(
        default="risk_assessment",
        description="Type of analysis: risk_assessment, optimization, performance, comprehensive"
    )
    risk_tolerance: Optional[str] = Field(default="moderate", description="Risk tolerance level")
    investment_horizon: Optional[str] = Field(default="medium", description="Investment horizon")


class MarketResearchInput(AgentInput):
    """Input schema for market research."""
    
    query: str = Field(..., description="Research query or topic")
    market_type: str = Field(default="crypto", description="Market type: crypto, stocks, forex")
    sources: Optional[List[str]] = Field(default=None, description="Specific sources to search")
    depth: str = Field(default="standard", description="Research depth: quick, standard, deep")


class RiskAssessmentInput(AgentInput):
    """Input schema for risk assessment."""
    
    asset_data: Dict[str, Any] = Field(..., description="Asset data for risk assessment")
    risk_metrics: List[str] = Field(default=["volatility", "var", "sharpe"], description="Risk metrics to calculate")
    confidence_level: float = Field(default=0.95, description="Confidence level for risk calculations")
    time_horizon: Optional[str] = Field(default="1y", description="Time horizon for risk assessment")
