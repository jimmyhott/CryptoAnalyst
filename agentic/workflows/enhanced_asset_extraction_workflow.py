"""Enhanced Asset Extraction Workflow with sophisticated parsing capabilities."""

from typing import Dict, Any, List, Optional
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import json
import os
import re
from datetime import datetime

from .global_state import GlobalState
from ..prompts import (
    ASSET_EXTRACTION_PROMPT,
    ASSET_EXTRACTION_PROMPT_FAST,
    ASSET_EXTRACTION_PROMPT_DETAILED
)
from ..data.crypto_assets import (
    get_asset_database_json,
    get_sector_mappings_json,
    get_asset_list,
    get_asset_by_ticker,
    get_assets_by_sector,
    is_stablecoin,
    should_trigger_hitl,
    CRYPTO_ASSETS,
    SECTOR_MAPPINGS
)


class EnhancedAssetExtractionWorkflow:
    """Enhanced workflow for sophisticated asset extraction and analysis."""
    
    def __init__(self, openai_api_key: str = None):
        """Initialize the enhanced workflow."""
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
        """Build the enhanced LangGraph workflow."""
        
        # Create the state graph
        workflow = StateGraph(GlobalState)
        
        # Add nodes for each agent
        workflow.add_node("enhanced_asset_extraction", self._enhanced_asset_extraction_agent)
        workflow.add_node("human_in_the_loop", self._human_in_the_loop_agent)
        workflow.add_node("asset_validation", self._asset_validation_agent)
        workflow.add_node("price_retrieval", self._price_retrieval_agent)
        workflow.add_node("technical_analysis", self._technical_analysis_agent)
        workflow.add_node("news_retrieval", self._news_retrieval_agent)
        workflow.add_node("sentiment_analysis", self._sentiment_analysis_agent)
        workflow.add_node("comprehensive_reporter", self._comprehensive_reporter_agent)
        
        # Define the workflow flow
        workflow.set_entry_point("enhanced_asset_extraction")
        
        # Connect the agents with conditional routing
        workflow.add_edge("enhanced_asset_extraction", "asset_validation")
        workflow.add_edge("asset_validation", "human_in_the_loop")
        workflow.add_edge("human_in_the_loop", "price_retrieval")
        workflow.add_edge("price_retrieval", "technical_analysis")
        workflow.add_edge("technical_analysis", "news_retrieval")
        workflow.add_edge("news_retrieval", "sentiment_analysis")
        workflow.add_edge("sentiment_analysis", "comprehensive_reporter")
        workflow.add_edge("comprehensive_reporter", END)
        
        return workflow.compile()
    
    def _enhanced_asset_extraction_agent(self, state: GlobalState) -> GlobalState:
        """Enhanced asset extraction using sophisticated AI parsing."""
        user_input = state.get("messages", [{}])[-1].get("content", "") if state.get("messages") else ""
        
        # Create chain using enhanced prompt
        asset_chain = ASSET_EXTRACTION_PROMPT | self.llm | StrOutputParser()
        
        try:
            # Extract assets using AI
            asset_response = asset_chain.invoke({
                "user_input": user_input,
                "asset_database": get_asset_database_json(),
                "sector_mappings": get_sector_mappings_json()
            })
            
            # Parse JSON response
            asset_data = json.loads(asset_response)
            
            # Extract primary ticker for backward compatibility
            primary_ticker = "BTC"  # Default fallback
            if asset_data.get("extracted_assets"):
                primary_ticker = asset_data["extracted_assets"][0]["ticker"]
            
            # Update state with enhanced asset data
            state["ticker"] = primary_ticker
            state["extracted_assets"] = asset_data.get("extracted_assets", [])
            state["analysis_mode"] = asset_data.get("mode", "asset_specific")
            state["analysis_meta"] = asset_data.get("meta", {})
            state["parse_notes"] = asset_data.get("parse_notes", "")
            state["hitl_required"] = asset_data.get("hitl_required", False)
            state["hitl_reason"] = asset_data.get("hitl_reason", "")
            
            # Add agent message
            state["messages"].append({
                "role": "agent",
                "agent": "enhanced_asset_extraction",
                "content": f"Enhanced AI extracted {len(asset_data.get('extracted_assets', []))} assets: {[asset['ticker'] for asset in asset_data.get('extracted_assets', [])]}",
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": {
                    "mode": asset_data.get("mode"),
                    "confidence_scores": [asset.get("confidence", 0) for asset in asset_data.get("extracted_assets", [])],
                    "hitl_required": asset_data.get("hitl_required", False)
                }
            })
            
        except Exception as e:
            print(f"Enhanced asset extraction error: {e}")
            # Fallback to simple extraction
            state["ticker"] = "BTC"
            state["extracted_assets"] = [{"ticker": "BTC", "name": "Bitcoin", "confidence": 0.5}]
            state["analysis_mode"] = "asset_specific"
            state["hitl_required"] = True
            state["hitl_reason"] = "extraction_error"
            
            state["messages"].append({
                "role": "agent",
                "agent": "enhanced_asset_extraction",
                "content": f"Asset extraction failed, using fallback: BTC",
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": {"error": str(e)}
            })
        
        return state
    
    def _human_in_the_loop_agent(self, state: GlobalState) -> GlobalState:
        """Handle human-in-the-loop interactions when needed."""
        hitl_required = state.get("hitl_required", False)
        
        if not hitl_required:
            # Skip HITL if not required
            state["messages"].append({
                "role": "agent",
                "agent": "human_in_the_loop",
                "content": "No human intervention required, proceeding with analysis",
                "timestamp": datetime.utcnow().isoformat()
            })
            return state
        
        # Simulate HITL interaction (in real implementation, this would pause for user input)
        hitl_reason = state.get("hitl_reason", "unknown")
        extracted_assets = state.get("extracted_assets", [])
        
        # Generate HITL message based on reason
        if hitl_reason == "confidence_low":
            message = f"Low confidence in asset extraction. Extracted: {[asset['ticker'] for asset in extracted_assets]}. Proceeding with analysis."
        elif hitl_reason == "ambiguous_asset":
            message = f"Ambiguous asset detected. Extracted: {[asset['ticker'] for asset in extracted_assets]}. Proceeding with analysis."
        elif hitl_reason == "sector_request":
            message = f"Sector request detected. Representative assets: {[asset['ticker'] for asset in extracted_assets]}. Proceeding with analysis."
        else:
            message = f"Human-in-the-loop required for: {hitl_reason}. Proceeding with analysis."
        
        state["messages"].append({
            "role": "agent",
            "agent": "human_in_the_loop",
            "content": message,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": {
                "hitl_reason": hitl_reason,
                "extracted_assets": extracted_assets
            }
        })
        
        return state
    
    def _asset_validation_agent(self, state: GlobalState) -> GlobalState:
        """Validate extracted assets and check for warnings."""
        extracted_assets = state.get("extracted_assets", [])
        warnings = []
        
        for asset in extracted_assets:
            ticker = asset.get("ticker", "")
            confidence = asset.get("confidence", 0)
            
            # Check for stablecoin warnings
            if is_stablecoin(ticker):
                warnings.append(f"Stablecoin detected: {ticker} - Technical analysis may not be meaningful")
            
            # Check for low confidence
            if confidence < 0.85:
                warnings.append(f"Low confidence in {ticker}: {confidence}")
            
            # Check for meme coins
            asset_info = get_asset_by_ticker(ticker)
            if "Meme" in asset_info.get("sectors", []):
                warnings.append(f"Meme coin detected: {ticker} - High volatility expected")
        
        # Update state with warnings
        state["asset_warnings"] = warnings
        
        state["messages"].append({
            "role": "agent",
            "agent": "asset_validation",
            "content": f"Asset validation complete. Warnings: {len(warnings)}",
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": {"warnings": warnings}
        })
        
        return state
    
    def _price_retrieval_agent(self, state: GlobalState) -> GlobalState:
        """Fetch price data for all extracted assets."""
        extracted_assets = state.get("extracted_assets", [])
        all_price_data = {}
        
        for asset in extracted_assets:
            ticker = asset.get("ticker", "")
            price_data = self._fetch_price_data(ticker)
            all_price_data[ticker] = price_data
        
        # Update state
        state["price_history"] = all_price_data.get(state.get("ticker", "BTC"), [])
        state["all_price_data"] = all_price_data
        
        state["messages"].append({
            "role": "agent",
            "agent": "price_retrieval",
            "content": f"Retrieved price data for {len(extracted_assets)} assets",
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": {"assets_processed": len(extracted_assets)}
        })
        
        return state
    
    def _technical_analysis_agent(self, state: GlobalState) -> GlobalState:
        """Calculate technical indicators for all assets."""
        all_price_data = state.get("all_price_data", {})
        all_indicators = {}
        
        for ticker, price_data in all_price_data.items():
            indicators = self._calculate_technical_indicators(price_data)
            all_indicators[ticker] = indicators
        
        # Update state
        state["technical_indicators"] = all_indicators.get(state.get("ticker", "BTC"), {})
        state["all_technical_indicators"] = all_indicators
        
        state["messages"].append({
            "role": "agent",
            "agent": "technical_analysis",
            "content": f"Calculated technical indicators for {len(all_indicators)} assets",
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": {"assets_analyzed": len(all_indicators)}
        })
        
        return state
    
    def _news_retrieval_agent(self, state: GlobalState) -> GlobalState:
        """Gather news for all extracted assets."""
        extracted_assets = state.get("extracted_assets", [])
        all_news = {}
        
        for asset in extracted_assets:
            ticker = asset.get("ticker", "")
            news_articles = self._fetch_news_articles(ticker)
            all_news[ticker] = news_articles
        
        # Update state
        state["news_articles"] = all_news.get(state.get("ticker", "BTC"), [])
        state["all_news"] = all_news
        
        state["messages"].append({
            "role": "agent",
            "agent": "news_retrieval",
            "content": f"Retrieved news for {len(extracted_assets)} assets",
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": {"assets_with_news": len(all_news)}
        })
        
        return state
    
    def _sentiment_analysis_agent(self, state: GlobalState) -> GlobalState:
        """Analyze sentiment for all assets."""
        all_news = state.get("all_news", {})
        all_sentiment = {}
        
        for ticker, news_articles in all_news.items():
            sentiment_scores = self._analyze_sentiment(news_articles)
            all_sentiment[ticker] = sentiment_scores
        
        # Update state
        state["sentiment_scores"] = all_sentiment.get(state.get("ticker", "BTC"), {})
        state["all_sentiment"] = all_sentiment
        
        state["messages"].append({
            "role": "agent",
            "agent": "sentiment_analysis",
            "content": f"Analyzed sentiment for {len(all_sentiment)} assets",
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": {"assets_analyzed": len(all_sentiment)}
        })
        
        return state
    
    def _comprehensive_reporter_agent(self, state: GlobalState) -> GlobalState:
        """Generate comprehensive analysis report for all assets."""
        extracted_assets = state.get("extracted_assets", [])
        analysis_mode = state.get("analysis_mode", "asset_specific")
        analysis_meta = state.get("analysis_meta", {})
        asset_warnings = state.get("asset_warnings", [])
        
        # Generate comprehensive report
        report = self._generate_comprehensive_report(
            extracted_assets=extracted_assets,
            analysis_mode=analysis_mode,
            analysis_meta=analysis_meta,
            asset_warnings=asset_warnings,
            all_price_data=state.get("all_price_data", {}),
            all_technical_indicators=state.get("all_technical_indicators", {}),
            all_sentiment=state.get("all_sentiment", {})
        )
        
        # Update state
        state["comprehensive_report"] = report
        
        state["messages"].append({
            "role": "agent",
            "agent": "comprehensive_reporter",
            "content": report,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": {
                "report_length": len(report),
                "assets_covered": len(extracted_assets)
            }
        })
        
        return state
    
    # Helper methods (placeholder implementations)
    
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
                "content": f"Significant news about {ticker} cryptocurrency...",
                "source": "CryptoNews",
                "sentiment": "positive",
                "timestamp": "2024-01-01T10:00:00Z"
            }
        ]
    
    def _analyze_sentiment(self, news_articles: List[Dict]) -> Dict[str, float]:
        """Analyze sentiment (placeholder implementation)."""
        return {
            "overall_sentiment": 0.65,
            "positive_ratio": 0.6,
            "negative_ratio": 0.2,
            "neutral_ratio": 0.2,
            "confidence": 0.85
        }
    
    def _generate_comprehensive_report(self, **kwargs) -> str:
        """Generate comprehensive analysis report."""
        extracted_assets = kwargs.get("extracted_assets", [])
        analysis_mode = kwargs.get("analysis_mode", "asset_specific")
        asset_warnings = kwargs.get("asset_warnings", [])
        
        report = f"# Comprehensive Crypto Analysis Report\n\n"
        report += f"**Analysis Mode:** {analysis_mode}\n"
        report += f"**Assets Analyzed:** {len(extracted_assets)}\n\n"
        
        if asset_warnings:
            report += "## ⚠️ Warnings\n"
            for warning in asset_warnings:
                report += f"- {warning}\n"
            report += "\n"
        
        report += "## 📊 Asset Summary\n"
        for asset in extracted_assets:
            ticker = asset.get("ticker", "")
            name = asset.get("name", "")
            confidence = asset.get("confidence", 0)
            report += f"- **{ticker}** ({name}): Confidence {confidence:.2f}\n"
        
        report += "\n## 📈 Technical Analysis\n"
        report += "Technical indicators calculated for all assets.\n\n"
        
        report += "## 📰 Sentiment Analysis\n"
        report += "Sentiment analysis completed for all assets.\n\n"
        
        report += "## 💡 Recommendations\n"
        report += "Based on comprehensive analysis of all extracted assets.\n"
        
        return report
    
    def run(self, initial_state: GlobalState) -> GlobalState:
        """Run the complete enhanced workflow."""
        return self.workflow.invoke(initial_state)
    
    def get_workflow(self):
        """Get the compiled workflow graph."""
        return self.workflow


# Factory function
def create_enhanced_asset_extraction_workflow(openai_api_key: str = None) -> EnhancedAssetExtractionWorkflow:
    """Create and return a new enhanced asset extraction workflow instance."""
    return EnhancedAssetExtractionWorkflow(openai_api_key)
