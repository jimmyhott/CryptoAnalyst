# Secrets Directory

This directory is for storing sensitive configuration and secrets that should not be committed to version control.

## Purpose

- API keys (OpenAI, CoinGecko, etc.)
- Database credentials
- Private keys
- Configuration files with sensitive data

## Usage

1. Create your secret files here (e.g., `secret_config.py`, `api_keys.py`)
2. Add them to `.gitignore` to prevent accidental commits
3. Import them in your workflows as needed

## Example Structure

```
secrets/
├── __init__.py
├── secret_config.py     # Main configuration file
├── api_keys.py          # API keys and tokens (optional)
├── database_config.py   # Database credentials (optional)
├── .gitkeep            # Ensures directory is tracked
└── README.md           # This file
```

## Security Notes

- Never commit actual secrets to version control
- Use environment variables when possible
- Consider using a secrets management service for production
- Regularly rotate API keys and credentials
