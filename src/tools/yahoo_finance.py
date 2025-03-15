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


def yf_get_financial_metrics(
    ticker: str,
    end_date: Optional[str] = None,
    period: str = "ttm",
    limit: int = 10
) -> List[FinancialMetrics]:
    """
    Get financial metrics for a company from Yahoo Finance.
    
    Args:
        ticker: Stock ticker symbol
        end_date: End date for financial metrics (ignored, Yahoo Finance provides latest data)
        period: Reporting period (ttm, annual, quarterly)
        limit: Maximum number of metrics to return (ignored, Yahoo Finance provides one set)
        
    Returns:
        List of FinancialMetrics objects
    """
    cache_key = ticker
    if cache_key in _cache["financial_metrics"]:
        logger.info(f"Using cached financial metrics for {ticker}")
        return _cache["financial_metrics"][cache_key]
    
    try:
        logger.info(f"Fetching financial metrics for {ticker}")
        ticker_data = yf.Ticker(ticker)
        
        # Get key statistics and financial data
        info = ticker_data.info
        
        if not info:
            logger.warning(f"No financial metrics found for {ticker}")
            return []
        
        # Get the current date as report_period if end_date is not provided
        report_period = end_date if end_date else datetime.now().strftime('%Y-%m-%d')
        
        # Create financial metrics object with data from Yahoo Finance
        # Map Yahoo Finance fields to our FinancialMetrics model
        financial_metrics = FinancialMetrics(
            ticker=ticker,
            report_period=report_period,
            period=period,
            currency=info.get('currency', 'USD'),
            market_cap=info.get('marketCap'),
            enterprise_value=info.get('enterpriseValue'),
            price_to_earnings_ratio=info.get('trailingPE'),
            price_to_book_ratio=info.get('priceToBook'),
            price_to_sales_ratio=info.get('priceToSalesTrailing12Months'),
            enterprise_value_to_ebitda_ratio=info.get('enterpriseToEbitda'),
            enterprise_value_to_revenue_ratio=info.get('enterpriseToRevenue'),
            free_cash_flow_yield=None,  # Not directly available from Yahoo Finance
            peg_ratio=info.get('pegRatio'),
            gross_margin=info.get('grossMargins', 0) * 100 if info.get('grossMargins') else None,
            operating_margin=info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else None,
            net_margin=info.get('profitMargins', 0) * 100 if info.get('profitMargins') else None,
            return_on_equity=info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else None,
            return_on_assets=info.get('returnOnAssets', 0) * 100 if info.get('returnOnAssets') else None,
            return_on_invested_capital=None,  # Not directly available from Yahoo Finance
            asset_turnover=None,  # Not directly available from Yahoo Finance
            inventory_turnover=None,  # Not directly available from Yahoo Finance
            receivables_turnover=None,  # Not directly available from Yahoo Finance
            days_sales_outstanding=None,  # Not directly available from Yahoo Finance
            operating_cycle=None,  # Not directly available from Yahoo Finance
            working_capital_turnover=None,  # Not directly available from Yahoo Finance
            current_ratio=info.get('currentRatio'),
            quick_ratio=info.get('quickRatio'),
            cash_ratio=None,  # Not directly available from Yahoo Finance
            operating_cash_flow_ratio=None,  # Not directly available from Yahoo Finance
            debt_to_equity=info.get('debtToEquity'),
            debt_to_assets=None,  # Not directly available from Yahoo Finance
            interest_coverage=None,  # Not directly available from Yahoo Finance
            revenue_growth=info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else None,
            earnings_growth=info.get('earningsGrowth', 0) * 100 if info.get('earningsGrowth') else None,
            book_value_growth=None,  # Not directly available from Yahoo Finance
            earnings_per_share_growth=info.get('earningsQuarterlyGrowth', 0) * 100 if info.get('earningsQuarterlyGrowth') else None,
            free_cash_flow_growth=None,  # Not directly available from Yahoo Finance
            operating_income_growth=None,  # Not directly available from Yahoo Finance
            ebitda_growth=None,  # Not directly available from Yahoo Finance
            payout_ratio=info.get('payoutRatio', 0) * 100 if info.get('payoutRatio') else None,
            earnings_per_share=info.get('trailingEps'),
            book_value_per_share=info.get('bookValue'),
            free_cash_flow_per_share=None,  # Not directly available from Yahoo Finance
        )
        
        # Cache the results as a list for consistency with the API
        _cache["financial_metrics"][cache_key] = [financial_metrics]
        return [financial_metrics]
        
    except Exception as e:
        logger.error(f"Error fetching financial metrics for {ticker}: {str(e)}")
        return []


def clear_cache():
    """Clear all cached data."""
    _cache["prices"].clear()
    _cache["financial_metrics"].clear()
    _cache["line_items"].clear()
    _cache["market_cap"].clear()
    logger.info("Cleared Yahoo Finance cache")
