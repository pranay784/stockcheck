# Stock Dashboard - Streamlit Application

📊 **Interactive Stock Analysis Dashboard** - A comprehensive web application for analyzing stock data with charts and financial metrics.

## ✨ Features

- **Financial Data Analysis**: Real-time stock quotes, valuation ratios, performance metrics
- **Interactive Charts**: Price trends, volume analysis, valuation comparisons, performance distributions
- **Analyst Insights**: Recommendations, trading signals, and ratings
- **Risk Assessment**: Beta, volatility, and dividend analysis
- **Mobile Responsive**: Works perfectly on all devices

## 🚀 Quick Start

### Local Development

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

3. **Open Browser**: Navigate to `http://localhost:8501`

### Using Sample Data (Optional)
The app includes fallback mock data for demo purposes when API calls fail.

## 📱 Usage

1. **Enter Ticker Symbol**: Input any stock ticker (e.g., AAPL, MSFT, TSLA)
2. **Analyze Stock**: Click "🔍 Analyze Stock" to fetch data
3. **Explore Tabs**:
   - **📊 Overview**: Company information and key metrics
   - **📈 Charts**: Interactive visualizations
   - **🔍 Analysis**: Detailed performance analysis
   - **ℹ️ Details**: Complete data and descriptions

## 🚢 Deployment Options

### Option 1: Streamlit Cloud (Recommended - Easiest)
1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add Stock Dashboard Streamlit app"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Set main file path to `app.py`
   - Click Deploy!

### Option 2: Heroku Deployment
1. **Create Heroku App**:
   ```bash
   heroku create your-stock-dashboard
   ```

2. **Set Buildpack**:
   ```bash
   heroku buildpacks:set https://github.com/heroku/heroku-buildpack-python
   ```

3. **Deploy**:
   ```bash
   git push heroku main
   ```

4. **Open App**:
   ```bash
   heroku open
   ```

### Option 3: Other Platforms
- **Railway**: Auto-deploys from GitHub
- **Render**: Similar to Railway, great free tier
- **AWS/GCP/Azure**: Use their serverless/container services

## 📊 Data Sources

- **Finviz Finance**: Primary data provider for financial metrics
- **Fallback System**: Mock data when API unavailable

## 🛠️ Project Structure

```
stock2/
├── app.py                     # Main Streamlit application
├── stock_dashboard.py         # CLI version (reference)
├── test_dashboard.py          # CLI tests (reference)
├── requirements.txt           # Python dependencies
├── .streamlit/
│   └── config.toml           # Streamlit configuration
└── README.md                 # This file
```

## 🐍 Requirements

- Python 3.8+
- Streamlit 1.28+
- FinvizFinance 0.14.6
- Plotly 5.0.0
- Pandas 1.5.0

## 🎨 Customization

### Charts & Colors
Modify chart colors and styles in `app.py` within the `create_charts()` method.

### UI Layout
Update the sidebar and main layout in the `main()` function.

### Add Features
- Extend the `StreamlitStockDashboard` class
- Add new tabs to the interface
- Integrate additional data sources

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source - feel free to use and modify as needed.

## 🆘 Troubleshooting

**Common Issues:**

1. **Streamlit not found**: Install with `pip install streamlit`
2. **API rate limits**: App uses fallback mock data automatically
3. **Port conflicts**: Change port in `.streamlit/config.toml`

**Still having issues?**
- Check the console for error messages
- Verify all dependencies are installed
- Try running with `streamlit run app.py --logger.level=debug`

---

**Enjoy analyzing stocks with your new interactive dashboard!** 🎯📈
