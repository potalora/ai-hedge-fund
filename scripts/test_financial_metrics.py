"""
Test script for Yahoo Finance financial metrics integration.

This script demonstrates how to use the Yahoo Finance adapter to retrieve financial metrics
for a set of test tickers and validates that the integration is working correctly.
"""

import os
import sys
from datetime import datetime, timedelta

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import our modules
from src.tools.yahoo_finance import yf_get_financial_metrics
from src.tools.api import get_financial_metrics

# Set environment variable to use Yahoo Finance
os.environ["USE_YAHOO_FINANCE"] = "true"

# Test tickers (known to be free without API key)
TEST_TICKERS = ["AAPL", "GOOGL", "MSFT", "NVDA", "TSLA"]

def main():
    """Run tests for Yahoo Finance financial metrics integration."""
    print("Testing Yahoo Finance Financial Metrics Integration")
    print("=" * 50)
    
    # Get current date for end_date parameter
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"End date: {end_date}")
    print()
    
    # Test direct adapter access
    print("Testing direct adapter access:")
    for ticker in TEST_TICKERS:
        try:
            metrics = yf_get_financial_metrics(ticker, end_date)
            if metrics and len(metrics) > 0:
                print(f"  {ticker}: Retrieved financial metrics")
                print(f"     Market cap: ${metrics[0].market_cap:,.2f}" if metrics[0].market_cap else f"     Market cap: Not available")
                print(f"     P/E ratio: {metrics[0].price_to_earnings_ratio:.2f}" if metrics[0].price_to_earnings_ratio else f"     P/E ratio: Not available")
                print(f"     P/B ratio: {metrics[0].price_to_book_ratio:.2f}" if metrics[0].price_to_book_ratio else f"     P/B ratio: Not available")
                print(f"     Currency: {metrics[0].currency}")
            else:
                print(f"  {ticker}: Failed to retrieve financial metrics")
        except Exception as e:
            print(f"  {ticker}: Error - {str(e)}")
    
    print()
    
    # Test through API layer
    print("Testing through API layer:")
    for ticker in TEST_TICKERS:
        try:
            metrics = get_financial_metrics(ticker, end_date)
            if metrics and len(metrics) > 0:
                print(f"  {ticker}: Retrieved financial metrics")
                print(f"     Market cap: ${metrics[0].market_cap:,.2f}" if metrics[0].market_cap else f"     Market cap: Not available")
                print(f"     P/E ratio: {metrics[0].price_to_earnings_ratio:.2f}" if metrics[0].price_to_earnings_ratio else f"     P/E ratio: Not available")
                print(f"     P/B ratio: {metrics[0].price_to_book_ratio:.2f}" if metrics[0].price_to_book_ratio else f"     P/B ratio: Not available")
                print(f"     Currency: {metrics[0].currency}")
            else:
                print(f"  {ticker}: Failed to retrieve financial metrics")
        except Exception as e:
            print(f"  {ticker}: Error - {str(e)}")
    
    print()
    print("Test completed!")

if __name__ == "__main__":
    main()
