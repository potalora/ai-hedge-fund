"""
Yahoo Finance adapter module.

This module provides functions to fetch financial data from Yahoo Finance,
transforming the results to match the data models expected by the application.
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any

import yfinance as yf
import pandas as pd

from src.data.models import Price, FinancialMetrics, LineItem

# Set up logging
logger = logging.getLogger(__name__)

# Cache to store retrieved data and reduce API calls
_cache: Dict[str, Dict[str, Any]] = {
    "prices": {},
    "financial_metrics": {},
    "line_items": {},
    "market_cap": {},
}


def yf_get_prices(ticker: str, start_date: str, end_date: str) -> List[Price]:
    """
    Get historical price data from Yahoo Finance.
    
    Args:
        ticker: Stock ticker symbol
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        List of Price objects
    """
    cache_key = f"{ticker}_{start_date}_{end_date}"
    if cache_key in _cache["prices"]:
        logger.info(f"Using cached price data for {ticker}")
        return _cache["prices"][cache_key]
    
    try:
        logger.info(f"Fetching price data for {ticker} from {start_date} to {end_date}")
        # Use yfinance directly
        ticker_data = yf.Ticker(ticker)
        df = ticker_data.history(start=start_date, end=end_date)
        
        if df.empty:
            logger.warning(f"No price data found for {ticker}")
            return []
        
        # Transform DataFrame to Price objects
        prices = []
        for date, row in df.iterrows():
            price = Price(
                open=float(row['Open']),
                close=float(row['Close']),
                high=float(row['High']),
                low=float(row['Low']),
                volume=int(row['Volume']),
                time=date.strftime('%Y-%m-%d')
            )
            prices.append(price)
        
        # Cache the results
        _cache["prices"][cache_key] = prices
        return prices
        
    except Exception as e:
        logger.error(f"Error fetching price data for {ticker}: {str(e)}")
        return []


def clear_cache():
    """Clear all cached data."""
    _cache["prices"].clear()
    _cache["financial_metrics"].clear()
    _cache["line_items"].clear()
    _cache["market_cap"].clear()
    logger.info("Cleared Yahoo Finance cache")
