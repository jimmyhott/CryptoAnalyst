#!/usr/bin/env python3
"""
Azure OpenAI Setup Verification Script
This script helps verify your Azure OpenAI configuration and provides troubleshooting steps.
"""

import os
import sys

def check_environment_variables():
    """Check if Azure OpenAI environment variables are set."""
    print("🔍 Checking Environment Variables...")
    
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT", 
        "AZURE_OPENAI_DEPLOYMENT_NAME"
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value[:10]}..." if len(value) > 10 else f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")
            missing_vars.append(var)
    
    return len(missing_vars) == 0

def test_with_env_vars():
    """Test Azure OpenAI using environment variables."""
    print("\n🔧 Testing with Environment Variables...")
    
    try:
        from openai import AzureOpenAI
        
        # Get values from environment
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        if not all([api_key, endpoint, deployment]):
            print("❌ Missing environment variables. Please set them first.")
            return False
        
        print(f"✅ Using API Key: {api_key[:10]}...")
        print(f"✅ Using Endpoint: {endpoint}")
        print(f"✅ Using Deployment: {deployment}")
        
        client = AzureOpenAI(
            api_key=api_key,
            api_version="2025-01-01-preview",
            azure_endpoint=endpoint
        )
        
        print("🔍 Testing API call...")
        
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "user", "content": "Hello! What is 2+2?"}
            ],
            temperature=0.1
        )
        
        print(f"✅ Success! Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def provide_troubleshooting_steps():
    """Provide troubleshooting steps for Azure OpenAI setup."""
    print("\n🔧 Troubleshooting Steps:")
    print("1. Verify your Azure OpenAI resource is active:")
    print("   - Go to Azure Portal > Azure OpenAI")
    print("   - Check if your resource is running")
    
    print("\n2. Verify your API key:")
    print("   - Go to Azure Portal > Azure OpenAI > Keys and Endpoint")
    print("   - Copy the Key 1 or Key 2")
    print("   - Make sure it's not expired")
    
    print("\n3. Verify your endpoint:")
    print("   - Should be: https://[resource-name].[region].cognitiveservices.azure.com")
    print("   - Don't include /openai at the end")
    
    print("\n4. Verify your deployment:")
    print("   - Go to Azure Portal > Azure OpenAI > Deployments")
    print("   - Check the exact deployment name")
    print("   - Common names: gpt-4, gpt-35-turbo, gpt-4o, gpt-4o-mini")
    
    print("\n5. Set environment variables:")
    print("   export AZURE_OPENAI_API_KEY='your-api-key'")
    print("   export AZURE_OPENAI_ENDPOINT='your-endpoint'")
    print("   export AZURE_OPENAI_DEPLOYMENT_NAME='your-deployment-name'")
    
    print("\n6. Test with curl:")
    print("   curl -X POST \\")
    print("     -H 'api-key: YOUR_API_KEY' \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}]}' \\")
    print("     'https://YOUR_ENDPOINT/openai/deployments/YOUR_DEPLOYMENT/chat/completions?api-version=2025-01-01-preview'")

def main():
    """Main function to run the setup verification."""
    print("🚀 Azure OpenAI Setup Verification\n")
    
    # Check environment variables
    env_ok = check_environment_variables()
    
    if env_ok:
        # Test with environment variables
        test_ok = test_with_env_vars()
        
        if test_ok:
            print("\n🎉 Azure OpenAI is working correctly!")
            print("You can now use it in your crypto analysis workflow.")
        else:
            print("\n❌ Test failed. Check the troubleshooting steps below.")
            provide_troubleshooting_steps()
    else:
        print("\n❌ Environment variables not set.")
        provide_troubleshooting_steps()

if __name__ == "__main__":
    main()
