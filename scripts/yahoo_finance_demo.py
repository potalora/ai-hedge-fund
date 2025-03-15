"""
Test script for Yahoo Finance integration.

This script demonstrates how to use the Yahoo Finance adapter to retrieve price data
for a set of test tickers and validates that the integration is working correctly.
"""

import os
import sys
from datetime import datetime, timedelta

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now we can import from src
from src.tools.yahoo_finance import yf_get_prices
from src.tools.api import get_prices

# Set environment variable to use Yahoo Finance
os.environ["USE_YAHOO_FINANCE"] = "true"

# Test tickers (known to be free without API key)
TEST_TICKERS = ["AAPL", "GOOGL", "MSFT", "NVDA", "TSLA"]

def main():
    """Run tests for Yahoo Finance integration."""
    print("Testing Yahoo Finance Integration")
    print("=" * 50)
    
    # Set date range (last 30 days)
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    print(f"Date range: {start_date} to {end_date}")
    print()
    
    # Test direct adapter access
    print("Testing direct adapter access:")
    for ticker in TEST_TICKERS:
        try:
            prices = yf_get_prices(ticker, start_date, end_date)
            if prices:
                print(f"  {ticker}: Retrieved {len(prices)} price points")
                print(f"     Latest price: ${prices[0].close:.2f} on {prices[0].time}")
            else:
                print(f"  {ticker}: Failed to retrieve price data")
        except Exception as e:
            print(f"  {ticker}: Error - {str(e)}")
    
    print()
    
    # Test through API layer
    print("Testing through API layer:")
    for ticker in TEST_TICKERS:
        try:
            prices = get_prices(ticker, start_date, end_date)
            if prices:
                print(f"  {ticker}: Retrieved {len(prices)} price points")
                print(f"     Latest price: ${prices[0].close:.2f} on {prices[0].time}")
            else:
                print(f"  {ticker}: Failed to retrieve price data")
        except Exception as e:
            print(f"  {ticker}: Error - {str(e)}")
    
    print()
    print("Test completed!")

if __name__ == "__main__":
    main()
