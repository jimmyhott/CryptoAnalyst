"""Prompt templates for AI agents."""

import os
from pathlib import Path

# Import data structures and utilities from the data module
from ..data.crypto_assets import (
    get_asset_database_json,
    get_sector_mappings_json,
    get_asset_list,
    get_asset_by_ticker,
    get_assets_by_sector,
    is_stablecoin,
    should_trigger_hitl,
    CRYPTO_ASSETS,
    SECTOR_MAPPINGS,
    get_available_tickers,
    get_crypto_tickers,
    is_valid_ticker,
    CRYPTO_TICKERS
)

# Get the directory containing this file
PROMPTS_DIR = Path(__file__).parent

def _read_prompt_file(filename: str) -> str:
    """Read a prompt template from a text file."""
    file_path = PROMPTS_DIR / filename
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise FileNotFoundError(f"Prompt file not found: {file_path}")

def _extract_prompt_variant(full_text: str, variant_name: str) -> str:
    """Extract a specific prompt variant from the full text."""
    lines = full_text.split('\n')
    variant_lines = []
    in_variant = False
    
    for line in lines:
        if line.strip().startswith(f'# {variant_name}'):
            in_variant = True
            continue
        elif in_variant and line.strip().startswith('# '):
            break
        elif in_variant:
            variant_lines.append(line)
    
    return '\n'.join(variant_lines).strip()

# Load prompt templates from text files
ASSET_EXTRACTION_FULL = _read_prompt_file("asset_extraction.txt")
TICKER_EXTRACTION_FULL = _read_prompt_file("ticker_extraction.txt")

# Extract specific prompt variants
ASSET_EXTRACTION_PROMPT = _extract_prompt_variant(ASSET_EXTRACTION_FULL, "ASSET_EXTRACTION_PROMPT")
ASSET_EXTRACTION_PROMPT_FAST = _extract_prompt_variant(ASSET_EXTRACTION_FULL, "ASSET_EXTRACTION_PROMPT_FAST")
ASSET_EXTRACTION_PROMPT_DETAILED = _extract_prompt_variant(ASSET_EXTRACTION_FULL, "ASSET_EXTRACTION_PROMPT_DETAILED")

TICKER_EXTRACTION_PROMPT = _extract_prompt_variant(TICKER_EXTRACTION_FULL, "TICKER_EXTRACTION_PROMPT")
TICKER_EXTRACTION_PROMPT_SHORT = _extract_prompt_variant(TICKER_EXTRACTION_FULL, "TICKER_EXTRACTION_PROMPT_SHORT")
TICKER_EXTRACTION_PROMPT_WITH_EXAMPLES = _extract_prompt_variant(TICKER_EXTRACTION_FULL, "TICKER_EXTRACTION_PROMPT_WITH_EXAMPLES")

__all__ = [
    # Ticker extraction
    "TICKER_EXTRACTION_PROMPT",
    "TICKER_EXTRACTION_PROMPT_SHORT", 
    "TICKER_EXTRACTION_PROMPT_WITH_EXAMPLES",
    "get_available_tickers",
    "get_crypto_tickers",
    "is_valid_ticker",
    "CRYPTO_TICKERS",
    
    # Asset extraction
    "ASSET_EXTRACTION_PROMPT",
    "ASSET_EXTRACTION_PROMPT_FAST",
    "ASSET_EXTRACTION_PROMPT_DETAILED",
    "get_asset_database_json",
    "get_sector_mappings_json",
    "get_asset_list",
    "get_asset_by_ticker",
    "get_assets_by_sector",
    "is_stablecoin",
    "should_trigger_hitl",
    "CRYPTO_ASSETS",
    "SECTOR_MAPPINGS"
]
