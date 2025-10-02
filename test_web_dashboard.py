#!/usr/bin/env python3
"""
Test script for Web Dashboard
Tests the web dashboard functionality and chart generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web_dashboard import WebStockDashboard

def test_web_dashboard():
    """Test the web dashboard with Apple (AAPL)"""
    print("Testing Web Dashboard with AAPL (Apple Inc.)")
    print("=" * 50)

    # Create dashboard instance
    dashboard = WebStockDashboard()

    # Test data fetching
    print("Fetching data for AAPL...")
    success = dashboard.fetch_company_data("AAPL")

    if success:
        print("✅ Data fetch successful!")
        print(f"Company: {dashboard.quote_data.get('Company', 'N/A')}")
        print(f"Price: ${dashboard.quote_data.get('Price', 'N/A')}")

        # Test chart creation
        print("\nTesting chart creation...")
        charts = dashboard.create_charts()

        if charts:
            print("✅ Charts created successfully!")
            print(f"Available chart types: {list(charts.keys())}")

            # Check specific chart data
            if 'price_data' in charts:
                print(f"Price chart data points: {len(charts['price_data'])}")
            if 'volume_data' in charts:
                print(f"Volume chart data points: {len(charts['volume_data'])}")
            if 'valuation_data' in charts:
                print(f"Valuation chart data points: {len(charts['valuation_data'])}")
            if 'performance_data' in charts:
                print(f"Performance chart data points: {len(charts['performance_data'])}")

            return True
        else:
            print("❌ Chart creation failed")
            return False
    else:
        print("❌ Data fetch failed")
        return False

def test_dashboard_data():
    """Test the complete dashboard data generation"""
    print("\nTesting complete dashboard data generation...")
    dashboard = WebStockDashboard()

    result = dashboard.get_dashboard_data("AAPL")

    if result['success']:
        print("✅ Dashboard data generated successfully!")
        print(f"Ticker: {result['ticker']}")
        print(f"Data keys: {list(result['data'].keys())}")
        print(f"Chart keys: {list(result['charts'].keys())}")
        return True
    else:
        print(f"❌ Dashboard data generation failed: {result['error']}")
        return False

if __name__ == "__main__":
    test_web_dashboard()
    test_dashboard_data()
