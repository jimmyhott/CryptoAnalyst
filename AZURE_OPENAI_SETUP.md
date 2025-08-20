# Azure OpenAI Integration Setup Guide

## 🎯 Overview

This guide helps you set up Azure OpenAI integration for the CryptoAnalyst project. The system is now configured to use Azure OpenAI with the `gpt-4o` model for enhanced crypto analysis workflows.

## ✅ What's Been Implemented

### 1. **Azure OpenAI Configuration**
- ✅ Updated `agentic/secrets/secret_config.py` with Azure OpenAI settings
- ✅ Modified `agentic/workflows/ai_enhanced_workflow.py` to use `AzureChatOpenAI`
- ✅ Added environment variable support as fallback
- ✅ Created comprehensive test scripts

### 2. **Enhanced Workflow Features**
- ✅ **AI-Powered Ticker Extraction**: Uses LLM to extract crypto symbols from natural language
- ✅ **Sentiment Analysis**: Analyzes news and social media sentiment
- ✅ **Financial Reporting**: Generates comprehensive analysis reports
- ✅ **Human-in-the-Loop (HITL)**: Handles ambiguous cases with confidence scoring

### 3. **Test Scripts Created**
- ✅ `test_azure_openai.py` - Full workflow integration test
- ✅ `test_azure_direct.py` - Direct API connection test
- ✅ `test_azure_setup.py` - Setup verification and troubleshooting

## 🔧 Current Configuration

```python
# From agentic/secrets/secret_config.py
AZURE_OPENAI_API_KEY = "your-azure-openai-api-key-here"
AZURE_OPENAI_ENDPOINT = "https://your-resource-name.your-region.cognitiveservices.azure.com"
AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4o"
AZURE_OPENAI_API_VERSION = "2025-01-01-preview"
```

## 🚨 Current Issue: 401 Authentication Error

The system is getting a 401 "Access denied" error, which typically means:

1. **Invalid API Key**: The key might be expired or incorrect
2. **Wrong Endpoint**: The endpoint URL might be incorrect
3. **Resource Not Active**: The Azure OpenAI resource might be stopped
4. **Deployment Issues**: The deployment name might be wrong

## 🔍 Troubleshooting Steps

### Step 1: Verify Azure OpenAI Resource
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Azure OpenAI resource
3. Check if the resource is **Running** (not stopped)
4. Verify the resource is in the correct region

### Step 2: Get Correct API Key
1. In Azure Portal, go to your Azure OpenAI resource
2. Click on **"Keys and Endpoint"** in the left menu
3. Copy **Key 1** or **Key 2** (not the endpoint)
4. Make sure the key is not expired

### Step 3: Get Correct Endpoint
1. In the same "Keys and Endpoint" section
2. Copy the **Endpoint** URL
3. It should look like: `https://[resource-name].[region].cognitiveservices.azure.com`
4. **Don't** include `/openai` at the end

### Step 4: Get Correct Deployment Name
1. In Azure Portal, go to your Azure OpenAI resource
2. Click on **"Deployments"** in the left menu
3. Note the exact deployment name
4. Common names: `gpt-4`, `gpt-35-turbo`, `gpt-4o`, `gpt-4o-mini`

### Step 5: Test with curl
```bash
curl -X POST \
  -H 'api-key: YOUR_ACTUAL_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"Hello"}]}' \
  'https://YOUR_ENDPOINT/openai/deployments/YOUR_DEPLOYMENT/chat/completions?api-version=2025-01-01-preview'
```

### Step 6: Update Configuration
Once you have the correct values, update `agentic/secrets/secret_config.py`:

```python
AZURE_OPENAI_API_KEY = "your-actual-api-key"
AZURE_OPENAI_ENDPOINT = "your-actual-endpoint"
AZURE_OPENAI_DEPLOYMENT_NAME = "your-actual-deployment-name"
```

## 🧪 Testing the Integration

### Option 1: Use Environment Variables
```bash
export AZURE_OPENAI_API_KEY="your-api-key"
export AZURE_OPENAI_ENDPOINT="your-endpoint"
export AZURE_OPENAI_DEPLOYMENT_NAME="your-deployment"
python test_azure_setup.py
```

### Option 2: Test Full Workflow
```bash
python test_azure_openai.py
```

### Option 3: Test Direct API
```bash
python test_azure_direct.py
```

## 🎯 Expected Results

When working correctly, you should see:
```
✅ Azure OpenAI is working correctly!
✅ LLM Response: Bitcoin's ticker symbol is BTC
✅ Workflow executed successfully!
📊 Final ticker: BTC
💬 Messages count: 6
```

## 🔄 Next Steps

1. **Fix Authentication**: Follow the troubleshooting steps above
2. **Test Integration**: Run the test scripts to verify everything works
3. **Use in FastAPI**: The workflow is ready to be integrated into your FastAPI endpoints
4. **Deploy**: Once working, you can deploy the enhanced crypto analysis system

## 📚 Additional Resources

- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [LangChain Azure OpenAI Integration](https://python.langchain.com/docs/integrations/chat/azure_openai)
- [OpenAI Python SDK](https://github.com/openai/openai-python)

## 🆘 Need Help?

If you continue to have issues:
1. Check the Azure OpenAI resource status
2. Verify your subscription has access to Azure OpenAI
3. Ensure you have the correct permissions
4. Try creating a new deployment if needed

---

**Status**: 🔧 Configuration Complete, ⚠️ Authentication Issue Detected
**Next Action**: Fix Azure OpenAI authentication using the troubleshooting steps above
