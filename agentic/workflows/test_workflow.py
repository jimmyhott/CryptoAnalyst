#!/usr/bin/env python3
"""Comprehensive test suite for Crypto Analysis Workflow."""

import sys
import os
from typing import Dict, Any, List

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agentic.workflows.crypto_analysis_workflow import CryptoAnalysisWorkflow
from agentic.workflows.global_state import GlobalState


class WorkflowTester:
    """Test suite for the crypto analysis workflow."""
    
    def __init__(self):
        """Initialize the tester with a workflow instance."""
        self.workflow = CryptoAnalysisWorkflow()
    
    def create_initial_state(self, user_input: str = "Analyze Bitcoin for me") -> GlobalState:
        """Create an initial state for testing."""
        return {
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
    
    def test_ticker_extraction(self, test_cases: List[str]) -> None:
        """Test ticker extraction with different inputs."""
        print("🔍 Testing Ticker Extraction Agent")
        print("=" * 40)
        
        for i, user_input in enumerate(test_cases, 1):
            print(f"\n📝 Test Case {i}: '{user_input}'")
            
            # Create workflow instance for this test
            workflow = CryptoAnalysisWorkflow()
            initial_state = self.create_initial_state(user_input)
            
            # Run only the ticker extraction agent
            result_state = workflow._ticker_extraction_agent(initial_state)
            
            print(f"   ✅ Extracted Ticker: {result_state['ticker']}")
            print(f"   📋 Agent Message: {result_state['messages'][-1]['content']}")
    
    def test_individual_agents(self, ticker: str = "BTC") -> None:
        """Test each agent individually with sample data."""
        print(f"\n🤖 Testing Individual Agents for {ticker}")
        print("=" * 50)
        
        workflow = CryptoAnalysisWorkflow()
        
        # Test 1: Price Retrieval Agent
        print("\n📊 Testing Price Retrieval Agent...")
        state = {
            "ticker": ticker,
            "price_history": [],
            "technical_indicators": {},
            "news_articles": [],
            "sentiment_scores": {},
            "risk_profile": {},
            "user_feedback": {},
            "messages": []
        }
        result = workflow._price_retrieval_agent(state)
        print(f"   ✅ Retrieved {len(result['price_history'])} price points")
        print(f"   📈 Sample data: {result['price_history'][0] if result['price_history'] else 'None'}")
        
        # Test 2: Technical Analysis Agent
        print("\n📈 Testing Technical Analysis Agent...")
        result = workflow._technical_analysis_agent(result)
        print(f"   ✅ Calculated indicators: {list(result['technical_indicators'].keys())}")
        print(f"   📊 RSI: {result['technical_indicators'].get('rsi', 'N/A')}")
        
        # Test 3: News Retrieval Agent
        print("\n📰 Testing News Retrieval Agent...")
        result = workflow._news_retrieval_agent(result)
        print(f"   ✅ Retrieved {len(result['news_articles'])} articles")
        print(f"   📰 Sample article: {result['news_articles'][0]['title'] if result['news_articles'] else 'None'}")
        
        # Test 4: Sentiment Analysis Agent
        print("\n😊 Testing Sentiment Analysis Agent...")
        result = workflow._sentiment_analysis_agent(result)
        print(f"   ✅ Sentiment score: {result['sentiment_scores'].get('overall_sentiment', 'N/A')}")
        print(f"   🎯 Confidence: {result['sentiment_scores'].get('confidence', 'N/A')}")
        
        # Test 5: Financial Reporter Agent
        print("\n📋 Testing Financial Reporter Agent...")
        result = workflow._financial_reporter_agent(result)
        print(f"   ✅ Risk level: {result['risk_profile'].get('risk_level', 'N/A')}")
        print(f"   💡 Recommendation: {result['risk_profile'].get('recommendation', 'N/A')}")
        
        return result
    
    def test_complete_workflow(self, test_cases: List[Dict[str, Any]]) -> None:
        """Test the complete workflow with different scenarios."""
        print("\n🔄 Testing Complete Workflow")
        print("=" * 40)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 Test Scenario {i}: {test_case['name']}")
            print(f"   Input: {test_case['input']}")
            
            try:
                # Run complete workflow
                initial_state = self.create_initial_state(test_case['input'])
                final_state = self.workflow.run(initial_state)
                
                # Display results
                print(f"   ✅ Ticker: {final_state['ticker']}")
                print(f"   📊 Price Points: {len(final_state['price_history'])}")
                print(f"   📈 Indicators: {len(final_state['technical_indicators'])}")
                print(f"   📰 Articles: {len(final_state['news_articles'])}")
                print(f"   😊 Sentiment: {final_state['sentiment_scores'].get('overall_sentiment', 'N/A')}")
                print(f"   ⚠️ Risk: {final_state['risk_profile'].get('risk_level', 'N/A')}")
                print(f"   💡 Recommendation: {final_state['risk_profile'].get('recommendation', 'N/A')}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    def test_workflow_performance(self, iterations: int = 5) -> None:
        """Test workflow performance with multiple iterations."""
        print(f"\n⚡ Performance Test ({iterations} iterations)")
        print("=" * 40)
        
        import time
        
        total_time = 0
        successful_runs = 0
        
        for i in range(iterations):
            start_time = time.time()
            
            try:
                initial_state = self.create_initial_state(f"Analyze Bitcoin iteration {i+1}")
                final_state = self.workflow.run(initial_state)
                
                end_time = time.time()
                duration = end_time - start_time
                total_time += duration
                successful_runs += 1
                
                print(f"   Run {i+1}: {duration:.3f}s ✅")
                
            except Exception as e:
                print(f"   Run {i+1}: ❌ Error - {e}")
        
        if successful_runs > 0:
            avg_time = total_time / successful_runs
            print(f"\n📊 Performance Summary:")
            print(f"   Successful runs: {successful_runs}/{iterations}")
            print(f"   Average time: {avg_time:.3f}s")
            print(f"   Total time: {total_time:.3f}s")
    
    def test_error_handling(self) -> None:
        """Test error handling with invalid inputs."""
        print("\n🚨 Testing Error Handling")
        print("=" * 30)
        
        error_test_cases = [
            {"input": "", "expected": "empty input"},
            {"input": "Analyze XYZ123", "expected": "unknown ticker"},
            {"input": "Analyze", "expected": "incomplete input"},
        ]
        
        for test_case in error_test_cases:
            print(f"\n🧪 Testing: '{test_case['input']}' (expecting: {test_case['expected']})")
            
            try:
                initial_state = self.create_initial_state(test_case['input'])
                final_state = self.workflow.run(initial_state)
                print(f"   ✅ Workflow completed (ticker: {final_state['ticker']})")
                
            except Exception as e:
                print(f"   ❌ Error caught: {e}")
    
    def generate_test_report(self, final_state: GlobalState) -> str:
        """Generate a detailed test report."""
        report = f"""
# Crypto Analysis Workflow Test Report

## Test Summary
- **Ticker Analyzed**: {final_state['ticker']}
- **Price Data Points**: {len(final_state['price_history'])}
- **Technical Indicators**: {len(final_state['technical_indicators'])}
- **News Articles**: {len(final_state['news_articles'])}
- **Sentiment Score**: {final_state['sentiment_scores'].get('overall_sentiment', 'N/A')}
- **Risk Level**: {final_state['risk_profile'].get('risk_level', 'N/A')}
- **Recommendation**: {final_state['risk_profile'].get('recommendation', 'N/A')}

## Technical Indicators
{chr(10).join([f"- {k}: {v}" for k, v in final_state['technical_indicators'].items()])}

## Sentiment Analysis
{chr(10).join([f"- {k}: {v}" for k, v in final_state['sentiment_scores'].items()])}

## Risk Profile
{chr(10).join([f"- {k}: {v}" for k, v in final_state['risk_profile'].items()])}

## Agent Messages
{chr(10).join([f"{i+1}. {msg['agent']}: {msg['content']}" for i, msg in enumerate(final_state['messages'][1:])])}
        """
        return report.strip()


def run_comprehensive_tests():
    """Run all comprehensive tests."""
    print("🚀 Crypto Analysis Workflow - Comprehensive Test Suite")
    print("=" * 60)
    
    tester = WorkflowTester()
    
    # Test 1: Ticker Extraction
    ticker_test_cases = [
        "Analyze Bitcoin for me",
        "What's the status of Ethereum?",
        "Tell me about ADA",
        "How is DOT performing?",
        "Analyze LINK",
        "Check UNI",
        "What about LTC?",
        "Analyze BCH",
        "Tell me about some random coin XYZ123",
    ]
    tester.test_ticker_extraction(ticker_test_cases)
    
    # Test 2: Individual Agents
    final_state = tester.test_individual_agents("BTC")
    
    # Test 3: Complete Workflow
    workflow_test_cases = [
        {"name": "Bitcoin Analysis", "input": "Analyze Bitcoin for me"},
        {"name": "Ethereum Analysis", "input": "What's the status of Ethereum?"},
        {"name": "Cardano Analysis", "input": "Tell me about ADA"},
        {"name": "Polkadot Analysis", "input": "How is DOT performing?"},
    ]
    tester.test_complete_workflow(workflow_test_cases)
    
    # Test 4: Performance
    tester.test_workflow_performance(3)
    
    # Test 5: Error Handling
    tester.test_error_handling()
    
    # Generate final report
    print("\n📋 Final Test Report")
    print("=" * 30)
    report = tester.generate_test_report(final_state)
    print(report)
    
    print("\n🎉 All tests completed!")


if __name__ == "__main__":
    run_comprehensive_tests()
