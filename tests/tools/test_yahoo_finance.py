"""
Unit tests for the Yahoo Finance adapter module.
"""

import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest

from src.tools.yahoo_finance import yf_get_prices, clear_cache


class TestYahooFinanceAdapter(unittest.TestCase):
    """Test cases for Yahoo Finance adapter functions."""

    def setUp(self):
        """Set up test fixtures."""
        clear_cache()
        self.ticker = "AAPL"
        self.end_date = datetime.now().strftime("%Y-%m-%d")
        self.start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    @patch('yfinance.Ticker')
    def test_yf_get_prices_success(self, mock_ticker):
        """Test successful price data retrieval."""
        # Create mock Ticker instance
        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance
        
        # Create mock DataFrame with test data
        mock_data = pd.DataFrame({
            'Open': [150.0, 151.0, 152.0],
            'High': [155.0, 156.0, 157.0],
            'Low': [148.0, 149.0, 150.0],
            'Close': [153.0, 154.0, 155.0],
            'Volume': [1000000, 1100000, 1200000]
        }, index=pd.date_range(self.start_date, periods=3, freq='D'))
        
        # Set up the mock to return our data
        mock_ticker_instance.history.return_value = mock_data
        
        # Call the function
        prices = yf_get_prices(self.ticker, self.start_date, self.end_date)
        
        # Verify results
        self.assertEqual(len(prices), 3)
        self.assertEqual(prices[0].open, 150.0)
        self.assertEqual(prices[0].close, 153.0)
        self.assertEqual(prices[0].high, 155.0)
        self.assertEqual(prices[0].low, 148.0)
        self.assertEqual(prices[0].volume, 1000000)
        self.assertEqual(prices[0].time, pd.date_range(self.start_date, periods=1)[0].strftime('%Y-%m-%d'))

    @patch('yfinance.Ticker')
    def test_yf_get_prices_empty_data(self, mock_ticker):
        """Test handling of empty data."""
        # Create mock Ticker instance
        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance
        
        # Return empty DataFrame
        mock_ticker_instance.history.return_value = pd.DataFrame()
        
        # Call the function
        prices = yf_get_prices(self.ticker, self.start_date, self.end_date)
        
        # Verify results
        self.assertEqual(len(prices), 0)

    @patch('yfinance.Ticker')
    def test_yf_get_prices_exception(self, mock_ticker):
        """Test handling of exceptions."""
        # Create mock Ticker instance
        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance
        
        # Raise an exception
        mock_ticker_instance.history.side_effect = Exception("API error")
        
        # Call the function
        prices = yf_get_prices(self.ticker, self.start_date, self.end_date)
        
        # Verify results
        self.assertEqual(len(prices), 0)

    @patch('yfinance.Ticker')
    def test_yf_get_prices_caching(self, mock_ticker):
        """Test that caching works properly."""
        # Create mock Ticker instance
        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance
        
        # Create mock DataFrame with test data
        mock_data = pd.DataFrame({
            'Open': [150.0, 151.0, 152.0],
            'High': [155.0, 156.0, 157.0],
            'Low': [148.0, 149.0, 150.0],
            'Close': [153.0, 154.0, 155.0],
            'Volume': [1000000, 1100000, 1200000]
        }, index=pd.date_range(self.start_date, periods=3, freq='D'))
        
        # Set up the mock to return our data
        mock_ticker_instance.history.return_value = mock_data
        
        # First call should hit the API
        prices1 = yf_get_prices(self.ticker, self.start_date, self.end_date)
        
        # Second call should use the cache
        prices2 = yf_get_prices(self.ticker, self.start_date, self.end_date)
        
        # Verify the API was only called once
        mock_ticker_instance.history.assert_called_once()
        
        # Verify both calls returned the same data
        self.assertEqual(len(prices1), len(prices2))
        for i in range(len(prices1)):
            self.assertEqual(prices1[i].open, prices2[i].open)
            self.assertEqual(prices1[i].close, prices2[i].close)


if __name__ == '__main__':
    unittest.main()
