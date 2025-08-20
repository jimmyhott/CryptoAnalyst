#!/usr/bin/env python3
"""
Test script for Azure OpenAI integration with the enhanced crypto analysis workflow.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_azure_openai_integration():
    """Test the Azure OpenAI integration with the enhanced workflow."""
    print("🧪 Testing Azure OpenAI Integration...")
    
    try:
        # Import the enhanced workflow
        from agentic.workflows.ai_enhanced_workflow import AIEnhancedCryptoWorkflow
        print("✅ Successfully imported AIEnhancedCryptoWorkflow")
        
        # Initialize the workflow with Azure OpenAI
        workflow = AIEnhancedCryptoWorkflow()
        print("✅ Successfully initialized workflow with Azure OpenAI")
        
        # Test the LLM with a simple prompt
        print("🔍 Testing LLM with simple prompt...")
        test_prompt = "What is the ticker symbol for Bitcoin?"
        
        # Create a simple chain to test the LLM
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        
        prompt = ChatPromptTemplate.from_template("Answer this question: {question}")
        chain = prompt | workflow.llm | StrOutputParser()
        
        response = chain.invoke({"question": test_prompt})
        print(f"✅ LLM Response: {response}")
        
        # Test the workflow with a simple state
        print("🔍 Testing workflow execution...")
        initial_state = {
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
        
        # Execute the workflow
        result = workflow.workflow.invoke(initial_state)
        
        print("✅ Workflow executed successfully!")
        print(f"📊 Final ticker: {result.get('ticker', 'N/A')}")
        print(f"💬 Messages count: {len(result.get('messages', []))}")
        
        # Show the last few messages
        messages = result.get('messages', [])
        if messages:
            print("\n📝 Recent workflow messages:")
            for msg in messages[-3:]:  # Last 3 messages
                agent = msg.get('agent', 'unknown')
                content = msg.get('content', '')[:100] + "..." if len(msg.get('content', '')) > 100 else msg.get('content', '')
                print(f"  🤖 {agent}: {content}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_azure_config():
    """Test Azure configuration loading."""
    print("\n🔧 Testing Azure Configuration...")
    
    try:
        from agentic.secrets.secret_config import (
            AZURE_OPENAI_API_KEY,
            AZURE_OPENAI_ENDPOINT,
            AZURE_OPENAI_DEPLOYMENT_NAME
        )
        
        print(f"✅ Azure API Key: {AZURE_OPENAI_API_KEY[:10]}...")
        print(f"✅ Azure Endpoint: {AZURE_OPENAI_ENDPOINT}")
        print(f"✅ Deployment Name: {AZURE_OPENAI_DEPLOYMENT_NAME}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Configuration Import Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Azure OpenAI Integration Tests...\n")
    
    # Test configuration first
    config_ok = test_azure_config()
    
    if config_ok:
        # Test the full integration
        integration_ok = test_azure_openai_integration()
        
        if integration_ok:
            print("\n🎉 All tests passed! Azure OpenAI integration is working correctly.")
        else:
            print("\n❌ Integration test failed. Check the error messages above.")
            sys.exit(1)
    else:
        print("\n❌ Configuration test failed. Please check your Azure OpenAI setup.")
        sys.exit(1)
