"""AI-Enhanced Crypto Analysis Workflow using LangGraph and LangChain."""

from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import os

from .global_state import GlobalState
from ..prompts import TICKER_EXTRACTION_PROMPT
from ..data.crypto_assets import get_available_tickers, is_valid_ticker


class AIEnhancedCryptoWorkflow:
    """AI-enhanced workflow for cryptocurrency analysis."""
    
    def __init__(self, openai_api_key: str = None):
        """Initialize the AI-enhanced workflow."""
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1,
            api_key=self.openai_api_key
        )
        
        # Build workflow
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the AI-enhanced LangGraph workflow."""
        
        # Create the state graph
        workflow = StateGraph(GlobalState)
        
        # Add nodes for each agent
        workflow.add_node("ai_ticker_extraction", self._ai_ticker_extraction_agent)
        workflow.add_node("price_retrieval", self._price_retrieval_agent)
        workflow.add_node("technical_analysis", self._technical_analysis_agent)
        workflow.add_node("news_retrieval", self._news_retrieval_agent)
        workflow.add_node("ai_sentiment_analysis", self._ai_sentiment_analysis_agent)
        workflow.add_node("ai_financial_reporter", self._ai_financial_reporter_agent)
        
        # Define the workflow flow
        workflow.set_entry_point("ai_ticker_extraction")
        
        # Connect the agents in sequence
        workflow.add_edge("ai_ticker_extraction", "price_retrieval")
        workflow.add_edge("price_retrieval", "technical_analysis")
        workflow.add_edge("technical_analysis", "news_retrieval")
        workflow.add_edge("news_retrieval", "ai_sentiment_analysis")
        workflow.add_edge("ai_sentiment_analysis", "ai_financial_reporter")
        workflow.add_edge("ai_financial_reporter", END)
        
        return workflow.compile()
    
    def _ai_ticker_extraction_agent(self, state: GlobalState) -> GlobalState:
        """AI-powered ticker extraction using LLM."""
        user_input = state.get("messages", [{}])[-1].get("content", "") if state.get("messages") else ""
        
        # Create chain using extracted prompt
        ticker_chain = TICKER_EXTRACTION_PROMPT | self.llm | StrOutputParser()
        
        # Extract ticker using AI
        try:
            ticker = ticker_chain.invoke({"user_input": user_input}).strip()
            # Clean up the response
            ticker = ticker.replace('"', '').replace("'", "").strip()
            
            # Validate ticker using imported function
            if not is_valid_ticker(ticker):
                ticker = "BTC"  # Fallback
                
        except Exception as e:
            print(f"AI ticker extraction error: {e}")
            ticker = "BTC"  # Fallback
        
        # Update state
        state["ticker"] = ticker
        
        # Add agent message
        state["messages"].append({
            "role": "agent",
            "agent": "ai_ticker_extraction",
            "content": f"AI extracted ticker: {ticker} from input: '{user_input}'",
            "timestamp": "2024-01-01T00:00:00Z"
        })
        
        return state
    
    def _price_retrieval_agent(self, state: GlobalState) -> GlobalState:
        """Fetch historical and real-time price data for the ticker."""
        ticker = state["ticker"]
        
        # Fetch price data (placeholder implementation)
        price_data = self._fetch_price_data(ticker)
        
        # Update state with price history
        state["price_history"] = price_data
        
        # Add agent message
        state["messages"].append({
            "role": "agent",
            "agent": "price_retrieval",
            "content": f"Retrieved {len(price_data)} price data points for {ticker}",
            "timestamp": "2024-01-01T00:00:00Z"
        })
        
        return state
    
    def _technical_analysis_agent(self, state: GlobalState) -> GlobalState:
        """Calculate technical indicators (RSI, Bollinger Bands, MACD)."""
        price_history = state["price_history"]
        
        # Calculate technical indicators (placeholder implementation)
        indicators = self._calculate_technical_indicators(price_history)
        
        # Update state with technical indicators
        state["technical_indicators"] = indicators
        
        # Add agent message
        state["messages"].append({
            "role": "agent",
            "agent": "technical_analysis",
            "content": f"Calculated technical indicators: {list(indicators.keys())}",
            "timestamp": "2024-01-01T00:00:00Z"
        })
        
        return state
    
    def _news_retrieval_agent(self, state: GlobalState) -> GlobalState:
        """Gather relevant news articles for the cryptocurrency."""
        ticker = state["ticker"]
        
        # Fetch news articles (placeholder implementation)
        news_articles = self._fetch_news_articles(ticker)
        
        # Update state with news articles
        state["news_articles"] = news_articles
        
        # Add agent message
        state["messages"].append({
            "role": "agent",
            "agent": "news_retrieval",
            "content": f"Retrieved {len(news_articles)} news articles for {ticker}",
            "timestamp": "2024-01-01T00:00:00Z"
        })
        
        return state
    
    def _ai_sentiment_analysis_agent(self, state: GlobalState) -> GlobalState:
        """AI-powered sentiment analysis using LLM."""
        news_articles = state["news_articles"]
        ticker = state["ticker"]
        
        # Prepare news content for analysis
        news_content = "\n\n".join([
            f"Title: {article['title']}\nContent: {article['content']}"
            for article in news_articles
        ])
        
        # AI prompt for sentiment analysis
        sentiment_prompt = ChatPromptTemplate.from_template("""
You are a financial sentiment analyst. Analyze the sentiment of news articles about {ticker}.

News Articles:
{news_content}

Analyze the sentiment and return a JSON response with the following structure:
{{
    "overall_sentiment": <float between -1 and 1, where -1 is very negative, 0 is neutral, 1 is very positive>,
    "positive_ratio": <float between 0 and 1, percentage of positive sentiment>,
    "negative_ratio": <float between 0 and 1, percentage of negative sentiment>,
    "neutral_ratio": <float between 0 and 1, percentage of neutral sentiment>,
    "confidence": <float between 0 and 1, confidence in the analysis>,
    "key_sentiment_drivers": ["list", "of", "key", "factors", "affecting", "sentiment"]
}}

Return only the JSON response:""")
        
        # Create chain
        sentiment_chain = sentiment_prompt | self.llm | StrOutputParser()
        
        try:
            # Analyze sentiment using AI
            sentiment_response = sentiment_chain.invoke({
                "ticker": ticker,
                "news_content": news_content
            })
            
            # Parse JSON response
            sentiment_scores = json.loads(sentiment_response)
            
        except Exception as e:
            print(f"AI sentiment analysis error: {e}")
            # Fallback to placeholder
            sentiment_scores = {
                "overall_sentiment": 0.65,
                "positive_ratio": 0.6,
                "negative_ratio": 0.2,
                "neutral_ratio": 0.2,
                "confidence": 0.85,
                "key_sentiment_drivers": ["market sentiment", "news coverage"]
            }
        
        # Update state with sentiment scores
        state["sentiment_scores"] = sentiment_scores
        
        # Add agent message
        state["messages"].append({
            "role": "agent",
            "agent": "ai_sentiment_analysis",
            "content": f"AI analyzed sentiment: {sentiment_scores.get('overall_sentiment', 'N/A')} with {sentiment_scores.get('confidence', 'N/A')} confidence",
            "timestamp": "2024-01-01T00:00:00Z"
        })
        
        return state
    
    def _ai_financial_reporter_agent(self, state: GlobalState) -> GlobalState:
        """AI-powered comprehensive financial report generation."""
        # Gather all analysis data
        ticker = state["ticker"]
        price_history = state["price_history"]
        technical_indicators = state["technical_indicators"]
        news_articles = state["news_articles"]
        sentiment_scores = state["sentiment_scores"]
        
        # Generate risk profile
        risk_profile = self._generate_risk_profile(
            price_history, technical_indicators, sentiment_scores
        )
        
        # Update state with risk profile
        state["risk_profile"] = risk_profile
        
        # AI prompt for comprehensive report
        report_prompt = ChatPromptTemplate.from_template("""
You are a senior financial analyst specializing in cryptocurrency analysis. Generate a comprehensive, professional analysis report for {ticker}.

Technical Analysis Data:
{technical_indicators}

Sentiment Analysis:
{sentiment_scores}

Risk Profile:
{risk_profile}

News Summary:
{news_summary}

Generate a comprehensive report that includes:
1. Executive Summary
2. Technical Analysis with interpretation
3. Sentiment Analysis insights
4. Risk Assessment
5. Investment Recommendation
6. Key Takeaways

Make the report professional, data-driven, and actionable. Use markdown formatting.

Report:""")
        
        # Create chain
        report_chain = report_prompt | self.llm | StrOutputParser()
        
        try:
            # Generate comprehensive report using AI
            report = report_chain.invoke({
                "ticker": ticker,
                "technical_indicators": json.dumps(technical_indicators, indent=2),
                "sentiment_scores": json.dumps(sentiment_scores, indent=2),
                "risk_profile": json.dumps(risk_profile, indent=2),
                "news_summary": f"Retrieved {len(news_articles)} relevant articles"
            })
            
        except Exception as e:
            print(f"AI report generation error: {e}")
            # Fallback to template
            report = self._generate_comprehensive_report(
                ticker, price_history, technical_indicators, 
                news_articles, sentiment_scores, risk_profile
            )
        
        # Add final report message
        state["messages"].append({
            "role": "agent",
            "agent": "ai_financial_reporter",
            "content": report,
            "timestamp": "2024-01-01T00:00:00Z"
        })
        
        return state
    
    # Helper methods (same as before, but with enhanced implementations)
    
    def _fetch_price_data(self, ticker: str) -> List[Dict]:
        """Fetch price data (placeholder implementation)."""
        return [
            {"timestamp": "2024-01-01", "price": 45000.0, "volume": 1000000},
            {"timestamp": "2024-01-02", "price": 46000.0, "volume": 1100000},
            {"timestamp": "2024-01-03", "price": 44000.0, "volume": 900000},
        ]
    
    def _calculate_technical_indicators(self, price_history: List[Dict]) -> Dict[str, float]:
        """Calculate technical indicators (placeholder implementation)."""
        return {
            "rsi": 65.5,
            "macd": 0.0023,
            "bollinger_upper": 47000.0,
            "bollinger_lower": 43000.0,
            "sma_20": 45000.0,
            "ema_12": 45200.0,
        }
    
    def _fetch_news_articles(self, ticker: str) -> List[Dict]:
        """Fetch news articles (placeholder implementation)."""
        return [
            {
                "title": f"Major development for {ticker}",
                "content": f"Significant news about {ticker} cryptocurrency with positive market sentiment...",
                "source": "CryptoNews",
                "sentiment": "positive",
                "timestamp": "2024-01-01T10:00:00Z"
            },
            {
                "title": f"{ticker} market analysis",
                "content": f"Market analysis for {ticker} shows mixed signals with moderate volatility...",
                "source": "CoinDesk",
                "sentiment": "neutral",
                "timestamp": "2024-01-01T09:00:00Z"
            }
        ]
    
    def _generate_risk_profile(self, price_history: List[Dict], 
                             technical_indicators: Dict[str, float],
                             sentiment_scores: Dict[str, float]) -> Dict[str, Any]:
        """Generate risk profile (placeholder implementation)."""
        return {
            "volatility_score": 0.7,
            "risk_level": "moderate",
            "recommendation": "hold",
            "stop_loss": 42000.0,
            "take_profit": 48000.0,
            "confidence": 0.8
        }
    
    def _generate_comprehensive_report(self, ticker: str, price_history: List[Dict],
                                     technical_indicators: Dict[str, float],
                                     news_articles: List[Dict],
                                     sentiment_scores: Dict[str, float],
                                     risk_profile: Dict[str, Any]) -> str:
        """Generate comprehensive financial report (fallback implementation)."""
        return f"""
# {ticker} Comprehensive Analysis Report

## Technical Analysis
- RSI: {technical_indicators.get('rsi', 'N/A')}
- MACD: {technical_indicators.get('macd', 'N/A')}
- Bollinger Bands: {technical_indicators.get('bollinger_upper', 'N/A')} - {technical_indicators.get('bollinger_lower', 'N/A')}

## Sentiment Analysis
- Overall Sentiment: {sentiment_scores.get('overall_sentiment', 'N/A')}
- Confidence: {sentiment_scores.get('confidence', 'N/A')}

## Risk Assessment
- Risk Level: {risk_profile.get('risk_level', 'N/A')}
- Recommendation: {risk_profile.get('recommendation', 'N/A')}
- Stop Loss: ${risk_profile.get('stop_loss', 'N/A')}
- Take Profit: ${risk_profile.get('take_profit', 'N/A')}

## News Summary
Retrieved {len(news_articles)} relevant articles with mixed sentiment.

## Final Recommendation
Based on technical indicators, sentiment analysis, and market conditions, 
the recommendation is to {risk_profile.get('recommendation', 'monitor')} {ticker}.
        """.strip()
    
    def run(self, initial_state: GlobalState) -> GlobalState:
        """Run the complete AI-enhanced workflow."""
        return self.workflow.invoke(initial_state)
    
    def get_workflow(self):
        """Get the compiled workflow graph."""
        return self.workflow


# Factory function for easy workflow creation
def create_ai_enhanced_workflow(openai_api_key: str = None) -> AIEnhancedCryptoWorkflow:
    """Create and return a new AI-enhanced crypto analysis workflow instance."""
    return AIEnhancedCryptoWorkflow(openai_api_key)
