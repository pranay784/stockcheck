#!/usr/bin/env python3
"""
Test script for Stock Dashboard
Tests the dashboard functionality with a known ticker (AAPL)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from stock_dashboard import StockDashboard

def test_dashboard():
    """Test the stock dashboard with Apple (AAPL)"""
    print("Testing Stock Dashboard with AAPL (Apple Inc.)")
    print("=" * 50)

    # Create dashboard instance
    dashboard = StockDashboard()

    # Set test values
    dashboard.company_name = "Apple Inc."
    dashboard.ticker = "AAPL"

    # Test data fetching
    print("Fetching data for AAPL...")
    success = dashboard.fetch_company_data()

    if success:
        print("✅ Data fetch successful!")
        print("\nTesting dashboard display...")
        dashboard.display_dashboard()
        return True
    else:
        print("❌ Data fetch failed")
        return False

if __name__ == "__main__":
    test_dashboard()
