#!/usr/bin/env python3
"""
Direct test of Azure OpenAI connection to debug authentication issues.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_azure_openai_direct():
    """Test Azure OpenAI connection directly using the openai library."""
    print("🔧 Testing Azure OpenAI Direct Connection...")
    
    try:
        from agentic.secrets.secret_config import (
            AZURE_OPENAI_API_KEY,
            AZURE_OPENAI_ENDPOINT,
            AZURE_OPENAI_DEPLOYMENT_NAME
        )
        
        print(f"✅ Azure API Key: {AZURE_OPENAI_API_KEY[:10]}...")
        print(f"✅ Azure Endpoint: {AZURE_OPENAI_ENDPOINT}")
        print(f"✅ Deployment Name: {AZURE_OPENAI_DEPLOYMENT_NAME}")
        
        # Test with direct OpenAI client
        from openai import AzureOpenAI
        
        client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version="2025-01-01-preview",
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )
        
        print("🔍 Testing direct API call...")
        
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[
                {"role": "user", "content": "Hello! What is the ticker symbol for Bitcoin?"}
            ],
            temperature=0.1
        )
        
        print(f"✅ Direct API Response: {response.choices[0].message.content}")
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_langchain_azure():
    """Test Azure OpenAI with LangChain."""
    print("\n🔧 Testing Azure OpenAI with LangChain...")
    
    try:
        from agentic.secrets.secret_config import (
            AZURE_OPENAI_API_KEY,
            AZURE_OPENAI_ENDPOINT,
            AZURE_OPENAI_DEPLOYMENT_NAME
        )
        
        from langchain_openai import AzureChatOpenAI
        
        llm = AzureChatOpenAI(
            azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
            openai_api_version="2025-01-01-preview",
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            temperature=0.1
        )
        
        print("🔍 Testing LangChain API call...")
        
        response = llm.invoke("What is the ticker symbol for Bitcoin?")
        
        print(f"✅ LangChain Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ LangChain Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Direct Azure OpenAI Tests...\n")
    
    # Test direct connection first
    direct_ok = test_azure_openai_direct()
    
    if direct_ok:
        # Test LangChain connection
        langchain_ok = test_langchain_azure()
        
        if langchain_ok:
            print("\n🎉 All direct tests passed! Azure OpenAI is working correctly.")
        else:
            print("\n❌ LangChain test failed. Check the error messages above.")
            sys.exit(1)
    else:
        print("\n❌ Direct connection test failed. Please check your Azure OpenAI setup.")
        sys.exit(1)
