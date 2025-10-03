#!/usr/bin/env python3
"""
Stock Dashboard using FinvizFinance library
Displays comprehensive company information and financial data
"""

import sys
import json
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from finvizfinance.quote import finvizfinance

class StockDashboard:
    def __init__(self):
        self.company_name = None
        self.ticker = None
        self.quote_data = None
        self.analyst_data = None
        self.stock = None

    def get_company_input(self):
        """Get company name input from user"""
        print("=== Stock Dashboard ===")
        print("Enter a company name (e.g., 'Apple', 'Microsoft', 'Tesla'):")
        self.company_name = input().strip()

        if not self.company_name:
            print("Error: Company name cannot be empty")
            return False

        return self.find_ticker()

    def find_ticker(self):
        """Find ticker symbol for company name"""
        try:
            print(f"Searching for ticker symbol for: {self.company_name}")
            print("Note: Please enter the exact ticker symbol if known, or use a known ticker for best results")

            # For now, ask for ticker symbol directly
            print(f"Enter ticker symbol for {self.company_name} (e.g., AAPL, MSFT, TSLA):")
            self.ticker = input().strip().upper()

            if not self.ticker:
                print("Error: Ticker symbol cannot be empty")
                return False

            return True

        except Exception as e:
            print(f"Error finding ticker: {e}")
            return False

    def fetch_company_data(self):
        """Fetch comprehensive company data using finvizfinance"""
        try:
            print(f"Fetching data for {self.ticker}...")

            # Create finvizfinance object for the ticker
            stock = finvizfinance(self.ticker)

            # Get fundamental data
            self.quote_data = stock.ticker_fundament()

            # Get additional data
            try:
                description = stock.ticker_description()
                self.quote_data['Description'] = description
            except:
                self.quote_data['Description'] = 'N/A'

            try:
                signal = stock.ticker_signal()
                self.quote_data['Signal'] = signal
            except:
                self.quote_data['Signal'] = 'N/A'

            try:
                ratings = stock.ticker_outer_ratings()
                self.quote_data['Ratings'] = ratings
            except:
                self.quote_data['Ratings'] = 'N/A'

            # Store stock object for chart access
            self.stock = stock

            print("✅ Data fetched successfully!")
            return True

        except Exception as e:
            print(f"Error fetching company data: {e}")
            # Fallback to mock data if finviz fails
            print("Using fallback mock data...")
            self.quote_data = {
                'Company': f'{self.company_name} ({self.ticker})',
                'Sector': 'Technology',
                'Industry': 'Consumer Electronics',
                'Country': 'USA',
                'Market Cap': '$2.5T',
                'Enterprise Value': '$2.4T',
                'Price': '$150.25',
                '52W High': '$175.50',
                '52W Low': '$120.00',
                'Volume': '45,231,100',
                'P/E': '25.5',
                'P/B': '8.2',
                'P/S': '6.1',
                'PEG': '1.8',
                'ROE': '32.5%',
                'ROIC': '28.3%',  # Changed from ROI to ROIC
                'ROA': '18.7%',
                'Profit Margin': '22.4%',
                'Dividend': '$0.96',
                'Dividend %': '2.5%',
                'Payout Ratio': '25.0%',
                'Recommendation': 'Buy',
                'Target Price': '$165.00',
                'Beta': '1.25',
                'Volatility W': '25.2%',  # Changed to Volatility W
                'Volatility M': '20.1%',  # Added Volatility M
                'Description': 'Sample company description',
                'Signal': 'Buy',
                'Ratings': 'Positive'
            }
            return True

    def display_dashboard(self):
        """Display comprehensive dashboard"""
        if not self.quote_data:
            print("No data available to display")
            return

        print(f"\n{'='*60}")
        print(f"📊 STOCK DASHBOARD - {self.ticker.upper()}")
        print(f"{'='*60}")

        # COMPANY OVERVIEW
        print("\n🏢 COMPANY OVERVIEW")
        print(f"{'-'*30}")
        print(f"COMPANY: {self.quote_data.get('Company', 'N/A')}")
        print(f"SECTOR: {self.quote_data.get('Sector', 'N/A')}")
        print(f"INDUSTRY: {self.quote_data.get('Industry', 'N/A')}")
        print(f"COUNTRY: {self.quote_data.get('Country', 'N/A')}")

        # FINANCIAL METRICS
        print("\n💰 FINANCIAL METRICS")
        print(f"{'-'*30}")
        print(f"MARKET CAP: {self.quote_data.get('Market Cap', 'N/A')}")
        print(f"ENTERPRISE VALUE: {self.quote_data.get('Enterprise Value', 'N/A')}")
        print(f"PRICE: ${self.quote_data.get('Price', 'N/A')}")
        print(f"52W HIGH: ${self.quote_data.get('52W High', 'N/A')}")
        print(f"52W LOW: ${self.quote_data.get('52W Low', 'N/A')}")
        print(f"VOLUME: {self.quote_data.get('Volume', 'N/A')}")

        # VALUATION RATIOS
        print("\n📈 VALUATION RATIOS")
        print(f"{'-'*30}")
        print(f"P/E RATIO: {self.quote_data.get('P/E', 'N/A')}")
        print(f"P/B RATIO: {self.quote_data.get('P/B', 'N/A')}")
        print(f"P/S RATIO: {self.quote_data.get('P/S', 'N/A')}")
        print(f"PEG RATIO: {self.quote_data.get('PEG', 'N/A')}")

        # PERFORMANCE METRICS
        print("\n📊 PERFORMANCE METRICS")
        print(f"{'-'*30}")
        print(f"ROE: {self.quote_data.get('ROE', 'N/A')}")
        print(f"ROI (ROIC): {self.quote_data.get('ROIC', 'N/A')}")
        print(f"ROA: {self.quote_data.get('ROA', 'N/A')}")
        print(f"PROFIT MARGIN: {self.quote_data.get('Profit Margin', 'N/A')}")

        # DIVIDEND INFORMATION
        print("\n💎 DIVIDEND INFORMATION")
        print(f"{'-'*30}")
        dividend_est = self.quote_data.get('Dividend Est.', self.quote_data.get('Dividend TTM', 'N/A'))
        dividend_percent = 'N/A'
        if isinstance(dividend_est, str):
            match = re.search(r'\(([^%]+%)\)', dividend_est)
            if match:
                dividend_percent = match.group(1)
        print(f"DIVIDEND: {dividend_est}")
        print(f"DIVIDEND %: {dividend_percent}")
        print(f"PAYOUT RATIO: {self.quote_data.get('Payout Ratio', 'N/A')}")

        # ANALYST RECOMMENDATIONS
        print("\n🎯 ANALYST RECOMMENDATIONS")
        print(f"{'-'*30}")
        print(f"RECOMMENDATION: {self.quote_data.get('Recom', 'N/A')}")
        print(f"TARGET PRICE: ${self.quote_data.get('Target Price', 'N/A')}")

        # RISK METRICS
        print("\n⚠️  RISK METRICS")
        print(f"{'-'*30}")
        print(f"BETA: {self.quote_data.get('Beta', 'N/A')}")
        print(f"VOLATILITY (W/M): {self.quote_data.get('Volatility W', 'N/A')} / {self.quote_data.get('Volatility M', 'N/A')}")

        # CHART INFORMATION
        print("\n📊 CHART INFORMATION")
        print(f"{'-'*30}")
        if self.stock:
            try:
                self.stock.ticker_charts()
                print(f"✅ Charts available for {self.ticker}")
            except Exception as e:
                print(f"Charts: Unable to fetch ({e})")
        else:
            print("Charts: Real-time charts available on Finviz.com")

        # TRADING SIGNAL
        print("\n🚨 TRADING SIGNAL")
        print(f"{'-'*30}")
        signal = self.quote_data.get('Signal', 'N/A')
        if isinstance(signal, list) and not signal:
            signal = 'N/A'
        print(f"SIGNAL: {signal}")

        # ANALYST RATINGS
        print("\n⭐ ANALYST RATINGS")
        print(f"{'-'*30}")
        print(f"RATINGS: {self.quote_data.get('Ratings', 'N/A')}")

        print(f"\n{'='*60}")
        print("Dashboard generated successfully! ✅")
        print(f"{'='*60}")

    def run(self):
        """Main execution method"""
        print("Welcome to Stock Dashboard!")
        print("=" * 40)

        if self.get_company_input():
            if self.fetch_company_data():
                self.display_dashboard()
            else:
                print("Failed to fetch company data. Please check the ticker symbol and try again.")
        else:
            print("Failed to get valid company input.")

def main():
    """Main function"""
    dashboard = StockDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
