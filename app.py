#!/usr/bin/env python3
"""
Streamlit Stock Dashboard Application
Interactive web interface for stock analysis with charts and visualizations
Converted from Flask to Streamlit for easier deployment
"""

import streamlit as st
import sys
import json
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from finvizfinance.quote import finvizfinance
import plotly


import requests

import os

import re

class TickerLookup:
    """Service for looking up stock ticker symbols using LLM."""
    OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
    MODEL = "deepseek/deepseek-chat-v3.1:free"

    def __init__(self):
        # Use st.secrets for the API key
        self.api_key = st.secrets.get("OPENROUTER_API_KEY")
        if not self.api_key:
            st.error("OpenRouter API key not found. Please add it to your .streamlit/secrets.toml file.")
            self.headers = {}
        else:
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/pranay784/stockcheck"
            }

    def find_ticker(self, company_name: str) -> dict:
        if not self.api_key:
            return {"success": False, "ticker": None, "error": "API key not configured."}
        if not company_name:
            return {"success": False, "ticker": None, "error": "Company name is required"}
        try:
            prompt = f"What is the stock ticker symbol for {company_name}? Only return the ticker symbol in capital letters, nothing else."
            messages = [{"role": "user", "content": prompt}]
            response = requests.post(
                self.OPENROUTER_API_URL,
                headers=self.headers,
                json={"model": self.MODEL, "messages": messages}
            )
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and result["choices"]:
                    ticker = result["choices"][0]["message"]["content"].strip().upper()
                    if ticker:
                        return {"success": True, "ticker": ticker, "error": None}
            return {"success": False, "ticker": None, "error": "Could not find ticker symbol"}
        except Exception as e:
            return {"success": False, "ticker": None, "error": str(e)}
        


class StreamlitStockDashboard:
    def __init__(self):
        self.ticker = None
        self.quote_data = None
        self.stock = None
        self.ticker_lookup = TickerLookup()  # Add this line


    def test_api_connection(self):
        """Test the Finviz API connection with known good tickers"""
        test_tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
        results = {}

        for ticker in test_tickers:
            try:
                stock = finvizfinance(ticker)
                data = stock.ticker_fundament()
                results[ticker] = {"status": "success", "company": data.get('Company', 'N/A')}
            except Exception as e:
                results[ticker] = {"status": "error", "error": str(e)}

        return results

    def validate_ticker(self, ticker):
        """Validate ticker format and check if it exists"""
        if not ticker:
            return False, "Ticker cannot be empty"

        # Basic validation - should be 1-5 characters, letters and numbers only
        # Some tickers can have dots (like BRK.A) but let's keep it simple
        if not ticker.replace('.', '').isalnum():
            return False, "Ticker contains invalid characters"

        # Check length (most tickers are 1-5 characters, some longer)
        if len(ticker) > 10:
            return False, "Ticker too long"

        return True, "Valid ticker format"

    def fetch_company_data(self, ticker):
        """Fetch comprehensive company data using finvizfinance"""
        try:
            with st.spinner(f"Fetching data for {ticker}..."):
                progress_bar = st.progress(0)

                # Create finvizfinance object for the ticker
                stock = finvizfinance(ticker)
                progress_bar.progress(25)

                # Get fundamental data
                self.quote_data = stock.ticker_fundament()
                self.ticker = ticker
                self.stock = stock
                progress_bar.progress(50)

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

                progress_bar.progress(100)
                st.success("✅ Data fetched successfully!")
                return True

        except Exception as e:
            st.error(f"Error fetching company data: {e}")
            # Fallback to mock data if finviz fails
            st.warning("Using fallback mock data...")
            self.quote_data = {
                'Company': f'Sample Company ({ticker})',
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
                'ROI': '28.3%',
                'ROA': '18.7%',
                'Profit Margin': '22.4%',
                'Dividend': '$0.96',
                'Dividend %': '2.5%',
                'Payout Ratio': '25.0%',
                'Recommendation': 'Buy',
                'Target Price': '$165.00',
                'Beta': '1.25',
                'Volatility': '25.2%',
                'Description': 'Sample company description',
                'Signal': 'Buy',
                'Ratings': 'Positive'
            }
            self.ticker = ticker
            st.success("✅ Using sample data!")
            return True

    def create_charts(self):
        """Create interactive charts for the dashboard"""
        if not self.quote_data:
            return {}

        charts = {}

        try:
            # Price Performance Chart
            price_fig = go.Figure()
            price_fig.add_trace(go.Scatter(
                x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                y=[100, 105, 102, 110, 108, 115],
                mode='lines+markers',
                name='Stock Price',
                line=dict(color='#17BECF', width=3)
            ))
            price_fig.update_layout(
                title=f'{self.ticker} Price Performance (6 Months)',
                xaxis_title='Month',
                yaxis_title='Price ($)',
                template='plotly_white',
                height=400
            )
            charts['price_chart'] = price_fig

            # Volume Chart
            volume_fig = go.Figure()
            volume_fig.add_trace(go.Bar(
                x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                y=[1000000, 1200000, 900000, 1500000, 1300000, 1100000],
                name='Volume',
                marker_color='#FF6B6B'
            ))
            volume_fig.update_layout(
                title=f'{self.ticker} Trading Volume (6 Months)',
                xaxis_title='Month',
                yaxis_title='Volume',
                template='plotly_white',
                height=400
            )
            charts['volume_chart'] = volume_fig

            # Valuation Comparison Chart
            valuation_fig = go.Figure()
            valuation_fig.add_trace(go.Bar(
                x=['P/E', 'P/B', 'P/S', 'PEG'],
                y=[25.5, 8.2, 6.1, 1.8],
                marker_color=['#17BECF', '#FF6B6B', '#32CD32', '#FFD700']
            ))
            valuation_fig.update_layout(
                title=f'{self.ticker} Valuation Ratios',
                xaxis_title='Ratio',
                yaxis_title='Value',
                template='plotly_white',
                height=400
            )
            charts['valuation_chart'] = valuation_fig

            # Performance Metrics Pie Chart
            performance_fig = go.Figure()
            performance_fig.add_trace(go.Pie(
                labels=['ROE', 'ROI', 'ROA', 'Profit Margin'],
                values=[32.5, 28.3, 18.7, 22.4],
                marker_colors=['#17BECF', '#FF6B6B', '#32CD32', '#FFD700']
            ))
            performance_fig.update_layout(
                title=f'{self.ticker} Performance Metrics Distribution',
                template='plotly_white',
                height=400
            )
            charts['performance_chart'] = performance_fig

        except Exception as e:
            st.error(f"Error creating charts: {e}")
            charts = {}

        return charts

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Stock Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        .sidebar-header {
            font-size: 1.25rem;
            font-weight: bold;
            color: #1f77b4;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize dashboard
    if 'dashboard' not in st.session_state:
        st.session_state.dashboard = StreamlitStockDashboard()
        st.session_state.ticker_input = ""
        st.session_state.show_data = False

    dashboard = st.session_state.dashboard

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-header">📊 Stock Dashboard</div>', unsafe_allow_html=True)
        st.markdown("### Enter Stock Information")

        # Company name lookup
        company_name = st.text_input("Company Name", placeholder="e.g., Apple, Microsoft, Tesla")
        if st.button("🔎 Find Ticker from Name"):
            if company_name:
                with st.spinner('Looking up ticker...'):
                    result = dashboard.ticker_lookup.find_ticker(company_name)
                    if result['success']:
                        st.success(f"Found ticker: {result['ticker']}")
                        st.session_state.ticker_input = result['ticker']
                        st.session_state.show_data = False
                    else:
                        st.error(f"Error: {result['error']}")

        ticker_input = st.text_input(
            "Company Ticker Symbol",
            placeholder="e.g., AAPL, MSFT, TSLA",
            help="Enter the stock ticker symbol you want to analyze",
            value=st.session_state.ticker_input
        ).upper()

        # Update session state when input changes
        if ticker_input != st.session_state.ticker_input:
            st.session_state.ticker_input = ticker_input
            st.session_state.show_data = False  # Reset data when input changes

        analyze_button = st.button("🔍 Analyze Stock", type="primary", use_container_width=True)

        st.markdown("---")

        # Test API button
        if st.button("🧪 Test API Connection", use_container_width=True):
            st.markdown("### API Test Results")

            with st.spinner("Testing API connection..."):
                test_results = dashboard.test_api_connection()

            # Display test results
            for ticker, result in test_results.items():
                if result["status"] == "success":
                    st.success(f"✅ {ticker}: {result['company']}")
                else:
                    st.error(f"❌ {ticker}: {result['error']}")

        st.markdown("### About")
        st.markdown("""
        This dashboard provides comprehensive stock analysis including:
        - 📈 Financial metrics and ratios
        - 📊 Interactive charts and visualizations
        - 🎯 Analyst recommendations
        - ⚠️ Risk metrics and signals
        - 🧪 API connectivity testing
        """)

    # Main content
    st.markdown('<div class="main-header">📊 Stock Analysis Dashboard</div>', unsafe_allow_html=True)

    if analyze_button and st.session_state.ticker_input:
        # Validate ticker before fetching data
        is_valid, validation_message = dashboard.validate_ticker(st.session_state.ticker_input)

        if not is_valid:
            st.error(f"❌ {validation_message}")
        else:
            if dashboard.fetch_company_data(st.session_state.ticker_input):
                st.session_state.show_data = True

    if st.session_state.show_data:
        # Create tabs for better organization
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Charts", "🔍 Analysis", "ℹ️ Details"])

        with tab1:
            st.subheader(f"🏢 Company Overview - {dashboard.ticker}")

            if dashboard.quote_data:
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("**Company Information**")
                    st.info(f"**Company:** {dashboard.quote_data.get('Company', 'N/A')}")
                    st.info(f"**Sector:** {dashboard.quote_data.get('Sector', 'N/A')}")
                    st.info(f"**Industry:** {dashboard.quote_data.get('Industry', 'N/A')}")
                    st.info(f"**Country:** {dashboard.quote_data.get('Country', 'N/A')}")

                with col2:
                    st.markdown("**Financial Metrics**")
                    st.info(f"**Market Cap:** {dashboard.quote_data.get('Market Cap', 'N/A')}")
                    st.info(f"**Price:** ${dashboard.quote_data.get('Price', 'N/A')}")
                    st.info(f"**Volume:** {dashboard.quote_data.get('Volume', 'N/A')}")
                    st.info(f"**52W High:** ${dashboard.quote_data.get('52W High', 'N/A')}")

                with col3:
                    st.markdown("**Valuation Ratios**")
                    st.info(f"**P/E:** {dashboard.quote_data.get('P/E', 'N/A')}")
                    st.info(f"**P/B:** {dashboard.quote_data.get('P/B', 'N/A')}")
                    st.info(f"**ROE:** {dashboard.quote_data.get('ROE', 'N/A')}")
                    st.info(f"**Recommendation:** {dashboard.quote_data.get('Recommendation', 'N/A')}")

        with tab2:
            st.subheader("📈 Interactive Charts")

            if dashboard.quote_data:
                charts = dashboard.create_charts()

                if charts:
                    col1, col2 = st.columns(2)

                    with col1:
                        st.plotly_chart(charts['price_chart'], use_container_width=True)
                        st.plotly_chart(charts['valuation_chart'], use_container_width=True)

                    with col2:
                        st.plotly_chart(charts['volume_chart'], use_container_width=True)
                        st.plotly_chart(charts['performance_chart'], use_container_width=True)
                else:
                    st.error("Unable to generate charts at this time.")

        with tab3:
            st.subheader("🔍 Detailed Analysis")

            if dashboard.quote_data:
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Performance Metrics**")
                    metrics_data = {
                        'ROE': dashboard.quote_data.get('ROE', 'N/A'),
                        'ROI (ROIC)': dashboard.quote_data.get('ROIC', 'N/A'),
                        'ROA': dashboard.quote_data.get('ROA', 'N/A'),
                        'Profit Margin': dashboard.quote_data.get('Profit Margin', 'N/A')
                    }
                    for metric, value in metrics_data.items():
                        st.metric(label=metric, value=value)

                with col2:
                    st.markdown("**Risk & Dividend**")
                    
                    # Extract and display dividend info
                    dividend_est = dashboard.quote_data.get('Dividend Est.', dashboard.quote_data.get('Dividend TTM', 'N/A'))
                    dividend_percent = 'N/A'
                    if isinstance(dividend_est, str):
                        match = re.search(r'\((\d+\.\d+)\%\)', dividend_est)
                        if match:
                            dividend_percent = f"{match.group(1)}%"

                    risk_data = {
                        'Beta': dashboard.quote_data.get('Beta', 'N/A'),
                        'Volatility (W/M)': f"{dashboard.quote_data.get('Volatility W', 'N/A')} / {dashboard.quote_data.get('Volatility M', 'N/A')}",
                        'Dividend': dividend_est.split(' ')[0] if isinstance(dividend_est, str) else 'N/A',
                        'Dividend %': dividend_percent
                    }
                    for metric, value in risk_data.items():
                        st.metric(label=metric, value=value)

                # Trading Signal
                st.markdown("**🚨 Trading Signal**")
                signal = dashboard.quote_data.get('Signal', 'N/A')
                
                # Handle empty list or non-string values from the API
                if not isinstance(signal, str) or not signal.strip():
                    signal = "N/A"

                if signal == 'Buy':
                    st.success(f"**Signal:** {signal}")
                elif signal == 'Sell':
                    st.error(f"**Signal:** {signal}")
                else:
                    st.info(f"**Signal:** {signal}")

        with tab4:
            st.subheader("ℹ️ Additional Details")

            if dashboard.quote_data:
                with st.expander("📋 Complete Financial Data"):
                    st.json(dashboard.quote_data)

                st.markdown("**📝 Description**")
                st.write(dashboard.quote_data.get('Description', 'N/A'))

                st.markdown("**⭐ Analyst Ratings**")
                st.write(dashboard.quote_data.get('Ratings', 'N/A'))

    elif analyze_button:
        st.warning("⚠️ Please enter a ticker symbol to analyze.")

    # Welcome message for first-time users
    if not ticker_input:
        st.markdown("""
        ### Welcome to the Stock Analysis Dashboard! 🚀

        **To get started:**
        1. Enter a stock ticker symbol in the sidebar (e.g., AAPL, MSFT, TSLA)
        2. Click "🔍 Analyze Stock" to fetch comprehensive data
        3. Explore the different tabs to view charts, metrics, and analysis

        **Features:**
        - 📊 Real-time financial data
        - 📈 Interactive charts and visualizations
        - 🎯 Analyst recommendations and signals
        - ⚠️ Risk metrics and analysis
        - 📱 Mobile-responsive design

        **Data Source:** Financial data provided by Finviz Finance
        """)

        # Sample tickers for users to try
        st.markdown("**Popular tickers to try:**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🍎 AAPL", use_container_width=True):
                st.session_state.ticker_input = "AAPL"
                st.rerun()
        with col2:
            if st.button("🪟 MSFT", use_container_width=True):
                st.session_state.ticker_input = "MSFT"
                st.rerun()
        with col3:
            if st.button("🚗 TSLA", use_container_width=True):
                st.session_state.ticker_input = "TSLA"
                st.rerun()
        with col4:
            if st.button("🎯 GOOGL", use_container_width=True):
                st.session_state.ticker_input = "GOOGL"
                st.rerun()

if __name__ == '__main__':
    main()
