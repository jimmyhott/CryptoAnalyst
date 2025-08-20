#!/usr/bin/env python3
"""Quick interactive test for Crypto Analysis Workflow."""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agentic.workflows.crypto_analysis_workflow import create_crypto_analysis_workflow
from agentic.workflows.global_state import GlobalState


def quick_test():
    """Run a quick test of the workflow."""
    print("🚀 Quick Crypto Analysis Workflow Test")
    print("=" * 40)
    
    # Get user input
    user_input = input("Enter your analysis request (e.g., 'Analyze Bitcoin'): ").strip()
    if not user_input:
        user_input = "Analyze Bitcoin for me"
    
    print(f"\n📝 Analyzing: '{user_input}'")
    print("-" * 30)
    
    # Create workflow and initial state
    workflow = create_crypto_analysis_workflow()
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
                "content": user_input,
                "timestamp": "2024-01-01T00:00:00Z"
            }
        ]
    }
    
    # Run workflow
    try:
        final_state = workflow.run(initial_state)
        
        # Display results
        print(f"✅ Ticker: {final_state['ticker']}")
        print(f"📊 Price Points: {len(final_state['price_history'])}")
        print(f"📈 Technical Indicators: {len(final_state['technical_indicators'])}")
        print(f"📰 News Articles: {len(final_state['news_articles'])}")
        print(f"😊 Sentiment: {final_state['sentiment_scores'].get('overall_sentiment', 'N/A')}")
        print(f"⚠️ Risk Level: {final_state['risk_profile'].get('risk_level', 'N/A')}")
        print(f"💡 Recommendation: {final_state['risk_profile'].get('recommendation', 'N/A')}")
        
        # Show final report
        print(f"\n📋 Final Report:")
        print("-" * 20)
        final_report = final_state['messages'][-1]['content']
        print(final_report)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def test_specific_agent():
    """Test a specific agent."""
    print("\n🤖 Test Specific Agent")
    print("=" * 25)
    
    agents = {
        "1": "Ticker Extraction",
        "2": "Price Retrieval", 
        "3": "Technical Analysis",
        "4": "News Retrieval",
        "5": "Sentiment Analysis",
        "6": "Financial Reporter"
    }
    
    print("Available agents:")
    for key, name in agents.items():
        print(f"  {key}. {name}")
    
    choice = input("\nSelect agent to test (1-6): ").strip()
    
    if choice not in agents:
        print("❌ Invalid choice")
        return
    
    workflow = create_crypto_analysis_workflow()
    
    # Create test state
    test_state = {
        "ticker": "BTC",
        "price_history": [],
        "technical_indicators": {},
        "news_articles": [],
        "sentiment_scores": {},
        "risk_profile": {},
        "user_feedback": {},
        "messages": []
    }
    
    # Test the selected agent
    agent_methods = {
        "1": workflow._ticker_extraction_agent,
        "2": workflow._price_retrieval_agent,
        "3": workflow._technical_analysis_agent,
        "4": workflow._news_retrieval_agent,
        "5": workflow._sentiment_analysis_agent,
        "6": workflow._financial_reporter_agent
    }
    
    try:
        result = agent_methods[choice](test_state)
        print(f"\n✅ {agents[choice]} completed successfully!")
        print(f"📊 Result state keys: {list(result.keys())}")
        
    except Exception as e:
        print(f"❌ Error testing {agents[choice]}: {e}")


if __name__ == "__main__":
    while True:
        print("\n" + "="*50)
        print("🔧 Crypto Analysis Workflow - Quick Test Menu")
        print("="*50)
        print("1. Quick Analysis Test")
        print("2. Test Specific Agent")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            quick_test()
        elif choice == "2":
            test_specific_agent()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
