#!/usr/bin/env python3
"""Test script for the Crypto Analysis Workflow."""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agentic.workflows.crypto_analysis_workflow import create_crypto_analysis_workflow
from agentic.workflows.global_state import GlobalState


def test_crypto_analysis_workflow():
    """Test the complete crypto analysis workflow."""
    
    print("🚀 Testing Crypto Analysis Workflow...")
    print("=" * 50)
    
    # Create workflow instance
    workflow = create_crypto_analysis_workflow()
    
    # Initialize state with user input
    initial_state: GlobalState = {
        "ticker": "",
        "price_history": [],
        "technical_indicators": {},
        "news_articles": [],
        "sentiment_scores": {},
        "risk_profile": {},
        "user_feedback": {},
        "messages": [
            {
                "role": "user",
                "content": "Analyze Bitcoin for me",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        ]
    }
    
    print(f"📝 Initial State:")
    print(f"   - User Input: {initial_state['messages'][0]['content']}")
    print(f"   - Ticker: {initial_state['ticker']}")
    print()
    
    # Run the complete workflow
    print("🔄 Running workflow...")
    final_state = workflow.run(initial_state)
    
    print("✅ Workflow completed!")
    print()
    
    # Display results
    print("📊 Final Results:")
    print(f"   - Extracted Ticker: {final_state['ticker']}")
    print(f"   - Price Data Points: {len(final_state['price_history'])}")
    print(f"   - Technical Indicators: {list(final_state['technical_indicators'].keys())}")
    print(f"   - News Articles: {len(final_state['news_articles'])}")
    print(f"   - Sentiment Score: {final_state['sentiment_scores'].get('overall_sentiment', 'N/A')}")
    print(f"   - Risk Level: {final_state['risk_profile'].get('risk_level', 'N/A')}")
    print(f"   - Recommendation: {final_state['risk_profile'].get('recommendation', 'N/A')}")
    print()
    
    # Display agent messages
    print("🤖 Agent Messages:")
    for i, message in enumerate(final_state['messages'][1:], 1):  # Skip user message
        print(f"   {i}. {message['agent']}: {message['content']}")
    print()
    
    # Display final report
    print("📋 Final Report:")
    print("-" * 30)
    final_report = final_state['messages'][-1]['content']
    print(final_report)
    
    return final_state


if __name__ == "__main__":
    try:
        test_crypto_analysis_workflow()
        print("\n🎉 Test completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
