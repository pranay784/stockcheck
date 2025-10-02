# 📊 Stock Dashboard - Web Application

A comprehensive web-based stock analysis dashboard with interactive charts and real-time financial data.

## 🚀 Features

### ✨ Core Functionality
- **Interactive Web Interface** - Beautiful, responsive design
- **Real-time Stock Data** - Powered by FinvizFinance API
- **Interactive Charts** - 4 types of Plotly visualizations
- **Comprehensive Analysis** - Complete financial metrics and ratios

### 📊 Dashboard Components

#### 🎯 Key Metrics Cards
- Market Capitalization
- P/E Ratio
- Trading Signal
- Analyst Recommendation

#### 📈 Interactive Charts
1. **Price Performance** - 6-month stock price trends
2. **Trading Volume** - Volume analysis over time
3. **Valuation Ratios** - P/E, P/B, P/S, PEG comparison
4. **Performance Metrics** - ROE, ROI, ROA distribution

#### 💼 Financial Information
- Enterprise Value, 52W High/Low, Volume
- Valuation Ratios (P/B, P/S, PEG)
- Performance Metrics (ROE, ROI, ROA, Profit Margin)
- Dividend Information
- Analyst Ratings and Target Prices

## 🛠️ Technical Stack

- **Backend:** Python Flask
- **Frontend:** HTML, CSS, JavaScript
- **Charts:** Plotly.js
- **Styling:** Tailwind CSS
- **Icons:** Font Awesome
- **Data Source:** FinvizFinance API

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
python web_dashboard.py
```

### Access the Dashboard
- **Local:** `http://127.0.0.1:5000`
- **Network:** `http://192.168.12.225:5000`

## 📋 Usage

1. **Open** the web application in your browser
2. **Enter** a company name (e.g., "Apple", "Microsoft") or ticker symbol (e.g., "AAPL", "MSFT")
3. **Click** "Generate Dashboard"
4. **View** comprehensive financial analysis with interactive charts
5. **Explore** hover tooltips, zoom functionality, and detailed metrics

## 🏗️ Project Structure

```
stock2/
├── web_dashboard.py          # Main Flask application
├── stock_dashboard.py        # Original command-line version
├── test_dashboard.py         # Test script for CLI version
├── test_web_dashboard.py     # Test script for web version
├── requirements.txt          # Python dependencies
├── templates/
│   ├── index.html           # Homepage with search form
│   ├── dashboard.html       # Main dashboard template
│   └── error.html           # Error handling page
└── README.md                # This file
```

## 🔧 API Endpoints

- `GET /` - Homepage with company search form
- `POST /dashboard` - Generate and display stock dashboard
- `GET /api/dashboard/<ticker>` - JSON API for dashboard data

## 🎨 Features

### Visual Design
- **Modern UI** with gradient backgrounds and card layouts
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Interactive Elements** - Hover effects and smooth transitions
- **Professional Styling** - Clean typography and consistent design

### Chart Visualizations
- **Price Performance** - Line chart with trend analysis
- **Trading Volume** - Bar chart with volume insights
- **Valuation Ratios** - Multi-colored comparison chart
- **Performance Metrics** - Pie chart distribution

### Error Handling
- **Graceful Degradation** - Fallback to mock data if API fails
- **User-Friendly Messages** - Clear error communication
- **Robust Validation** - Input validation and error recovery

## 🔐 Data Sources

- **Primary:** FinvizFinance API for real-time financial data
- **Fallback:** Mock data for demonstration when API unavailable
- **Charts:** Generated using Plotly.js for interactive visualizations

## 🚀 Deployment

### Local Development
```bash
python web_dashboard.py
```

### Production Deployment
For production deployment, consider:
- **WSGI Server** (Gunicorn, uWSGI)
- **Web Server** (Nginx, Apache)
- **Environment Variables** for API keys
- **SSL/TLS** encryption

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **FinvizFinance** for the financial data API
- **Plotly** for interactive chart library
- **Tailwind CSS** for the styling framework
- **Font Awesome** for the icon library

---

**Built with ❤️ for comprehensive stock market analysis**
