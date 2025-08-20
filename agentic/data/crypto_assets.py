"""Crypto asset data structures and utility functions."""

from typing import Dict, List, Any
import json


# Comprehensive crypto asset database
CRYPTO_ASSETS = {
    # Major cryptocurrencies
    "BTC": {"name": "Bitcoin", "aliases": ["bitcoin", "btc", "king", "king of crypto"], "confidence": 0.99},
    "ETH": {"name": "Ethereum", "aliases": ["ethereum", "eth", "etherium", "smart contract platform"], "confidence": 0.98},
    "ADA": {"name": "Cardano", "aliases": ["cardano", "ada"], "confidence": 0.95},
    "DOT": {"name": "Polkadot", "aliases": ["polkadot", "dot", "internet of blockchains"], "confidence": 0.95},
    "LINK": {"name": "Chainlink", "aliases": ["chainlink", "link", "oracle network"], "confidence": 0.94},
    "UNI": {"name": "Uniswap", "aliases": ["uniswap", "uni", "dex token"], "confidence": 0.93},
    "LTC": {"name": "Litecoin", "aliases": ["litecoin", "ltc"], "confidence": 0.92},
    "BCH": {"name": "Bitcoin Cash", "aliases": ["bitcoin cash", "bch"], "confidence": 0.91},
    
    # Layer 1s and DeFi
    "SOL": {"name": "Solana", "aliases": ["solana", "sol"], "confidence": 0.96},
    "MATIC": {"name": "Polygon", "aliases": ["polygon", "matic"], "confidence": 0.94},
    "AVAX": {"name": "Avalanche", "aliases": ["avalanche", "avax"], "confidence": 0.93},
    "ATOM": {"name": "Cosmos", "aliases": ["cosmos", "atom"], "confidence": 0.92},
    "ALGO": {"name": "Algorand", "aliases": ["algorand", "algo"], "confidence": 0.90},
    "XLM": {"name": "Stellar", "aliases": ["stellar", "xlm"], "confidence": 0.89},
    "VET": {"name": "VeChain", "aliases": ["vechain", "vet"], "confidence": 0.88},
    
    # AI and Emerging sectors
    "FET": {"name": "Fetch.ai", "aliases": ["fetch.ai", "fetch", "fet"], "confidence": 0.85, "sectors": ["AI"]},
    "NEAR": {"name": "NEAR Protocol", "aliases": ["near protocol", "near"], "confidence": 0.87, "sectors": ["AI", "Layer1"]},
    "RNDR": {"name": "Render", "aliases": ["render", "rndr"], "confidence": 0.86, "sectors": ["AI", "Compute"]},
    "OCEAN": {"name": "Ocean Protocol", "aliases": ["ocean protocol", "ocean"], "confidence": 0.84, "sectors": ["AI", "Data"]},
    "AGIX": {"name": "SingularityNET", "aliases": ["singularitynet", "agix"], "confidence": 0.83, "sectors": ["AI"]},
    
    # DeFi and Gaming
    "AAVE": {"name": "Aave", "aliases": ["aave"], "confidence": 0.92, "sectors": ["DeFi"]},
    "COMP": {"name": "Compound", "aliases": ["compound", "comp"], "confidence": 0.91, "sectors": ["DeFi"]},
    "SUSHI": {"name": "SushiSwap", "aliases": ["sushiswap", "sushi"], "confidence": 0.89, "sectors": ["DeFi"]},
    "AXS": {"name": "Axie Infinity", "aliases": ["axie infinity", "axs"], "confidence": 0.88, "sectors": ["Gaming"]},
    "MANA": {"name": "Decentraland", "aliases": ["decentraland", "mana"], "confidence": 0.87, "sectors": ["Gaming", "Metaverse"]},
    
    # Meme coins and trending
    "PEPE": {"name": "Pepe", "aliases": ["pepe"], "confidence": 0.80, "sectors": ["Meme"]},
    "DOGE": {"name": "Dogecoin", "aliases": ["dogecoin", "doge"], "confidence": 0.85, "sectors": ["Meme"]},
    "SHIB": {"name": "Shiba Inu", "aliases": ["shiba inu", "shib"], "confidence": 0.84, "sectors": ["Meme"]},
    
    # Stablecoins
    "USDT": {"name": "Tether", "aliases": ["tether", "usdt"], "confidence": 0.96, "sectors": ["Stablecoin"]},
    "USDC": {"name": "USD Coin", "aliases": ["usd coin", "usdc"], "confidence": 0.95, "sectors": ["Stablecoin"]},
    "DAI": {"name": "Dai", "aliases": ["dai"], "confidence": 0.94, "sectors": ["Stablecoin"]},
    
    # Layer 2s and Scaling
    "ARB": {"name": "Arbitrum", "aliases": ["arbitrum", "arb"], "confidence": 0.93, "sectors": ["Layer2"]},
    "OP": {"name": "Optimism", "aliases": ["optimism", "op"], "confidence": 0.92, "sectors": ["Layer2"]},
    "IMX": {"name": "Immutable", "aliases": ["immutable", "imx"], "confidence": 0.90, "sectors": ["Layer2", "Gaming"]},
}

# Sector mappings for broad requests
SECTOR_MAPPINGS = {
    "AI": ["FET", "NEAR", "RNDR", "OCEAN", "AGIX"],
    "DeFi": ["AAVE", "COMP", "SUSHI", "UNI"],
    "Gaming": ["AXS", "MANA", "IMX"],
    "Layer1": ["BTC", "ETH", "SOL", "ADA", "DOT", "AVAX"],
    "Layer2": ["ARB", "OP", "MATIC"],
    "Meme": ["PEPE", "DOGE", "SHIB"],
    "Stablecoin": ["USDT", "USDC", "DAI"],
}

# Common misspellings and corrections
MISSPELLINGS = {
    "etherium": "ETH",
    "bitcon": "BTC",
    "solana": "SOL",
    "polkadot": "DOT",
    "chainlink": "LINK",
    "uniswap": "UNI",
    "litecoin": "LTC",
    "bitcoin cash": "BCH",
    "polygon": "MATIC",
    "avalanche": "AVAX",
    "cosmos": "ATOM",
    "algorand": "ALGO",
    "stellar": "XLM",
    "vechain": "VET",
}

# Simple ticker mappings for backward compatibility
CRYPTO_TICKERS = {
    "Bitcoin": "BTC",
    "Ethereum": "ETH", 
    "Cardano": "ADA",
    "Polkadot": "DOT",
    "Chainlink": "LINK",
    "Uniswap": "UNI",
    "Litecoin": "LTC",
    "Bitcoin Cash": "BCH",
    "Solana": "SOL",
    "Polygon": "MATIC",
    "Avalanche": "AVAX",
    "Cosmos": "ATOM",
    "Algorand": "ALGO",
    "Stellar": "XLM",
    "VeChain": "VET"
}


# Utility functions
def get_asset_database_json() -> str:
    """Get asset database as formatted JSON string."""
    return json.dumps(CRYPTO_ASSETS, indent=2)

def get_sector_mappings_json() -> str:
    """Get sector mappings as formatted JSON string."""
    return json.dumps(SECTOR_MAPPINGS, indent=2)

def get_asset_list() -> str:
    """Get simple list of available tickers."""
    return ", ".join(CRYPTO_ASSETS.keys())

def get_asset_by_ticker(ticker: str) -> Dict[str, Any]:
    """Get asset information by ticker."""
    return CRYPTO_ASSETS.get(ticker.upper(), {})

def get_assets_by_sector(sector: str) -> List[str]:
    """Get assets in a specific sector."""
    return SECTOR_MAPPINGS.get(sector.upper(), [])

def is_stablecoin(ticker: str) -> bool:
    """Check if asset is a stablecoin."""
    asset = get_asset_by_ticker(ticker)
    return "Stablecoin" in asset.get("sectors", [])

def get_confidence_threshold() -> float:
    """Get confidence threshold for HITL triggers."""
    return 0.85

def should_trigger_hitl(confidence: float, asset_info: Dict[str, Any]) -> bool:
    """Determine if human-in-the-loop is required."""
    if confidence < get_confidence_threshold():
        return True
    if "Meme" in asset_info.get("sectors", []):
        return True
    if "collision_candidates" in asset_info:
        return True
    return False

def get_available_tickers() -> List[str]:
    """Get list of available ticker symbols."""
    return list(CRYPTO_TICKERS.values())

def get_crypto_tickers() -> Dict[str, str]:
    """Get dictionary of cryptocurrency names to ticker symbols."""
    return CRYPTO_TICKERS.copy()

def is_valid_ticker(ticker: str) -> bool:
    """Check if a ticker is valid."""
    return ticker in get_available_tickers()
