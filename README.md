---
title: Hyperliquid MCP Server & Trading Dashboard
emoji: 📊
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# 🚀 Hyperliquid MCP Server & Trading Dashboard

A production-ready **Model Context Protocol (MCP)** server with an interactive **Gradio dashboard** providing real-time trading data from **Hyperliquid** - the leading decentralized perpetual exchange.

## 🌐 Live Demo
**URL**: https://huggingface.co/spaces/rzvn/hyperliquid-mcp-server

## 🎯 Features

### ✅ MCP Server
- **8 Trading Tools** with RESTful API
- **Model Context Protocol** compliance
- **Real-time data** from Hyperliquid

### ✅ Interactive Dashboard
- **5 Interactive Tabs** with live data
- **Real-time charts** and visualizations
- **User-friendly interface** for all tools

## 📊 Available Trading Tools

### 1. **Market Prices** 📈
Get real-time prices for 200+ trading pairs
- Live price feed
- Top 20 by value
- Interactive data table

### 2. **Recent Trades** 💱
View recent trading activity
- Customizable trade count (1-1000)
- Real-time trade history
- Symbol-based filtering

### 3. **Candlestick Charts** 📊
Interactive price charts
- Multiple timeframes (1m, 5m, 1h, 4h, 1d)
- Customizable candle count
- Professional charting with Plotly

### 4. **Order Book** 📋
Live order book visualization
- Bid/ask depth charts
- Real-time updates
- Symbol-based lookup

### 5. **Funding Rates** 💰
Perpetual contract funding rates
- All markets overview
- Individual symbol focus
- Historical rate tracking

## 🔧 API Usage

### MCP Endpoints
- **Health Check**: `GET /health`
- **List Tools**: `POST /mcp/tools`
- **Execute Tool**: `POST /mcp/call`

### Example API Calls

#### Get All Market Prices
```bash
curl -X POST https://rzvn-hyperliquid-mcp-server.hf.space/mcp/call \
  -H "Content-Type: application/json" \
  -d '{"name": "get_all_mids", "arguments": {}}'
```

#### Get Recent BTC Trades
```bash
curl -X POST https://rzvn-hyperliquid-mcp-server.hf.space/mcp/call \
  -H "Content-Type: application/json" \
  -d '{"name": "get_recent_trades", "arguments": {"coin": "BTC", "n": 50}}'
```

## 🖥️ Interactive Dashboard Usage

### Dashboard Tabs

#### 📈 **Market Prices Tab**
- Click "Get All Market Prices" to load live data
- View top 20 cryptocurrencies by price
- Interactive sorting and filtering

#### 💱 **Recent Trades Tab**
- Enter coin symbol (e.g., "BTC", "ETH")
- Adjust number of trades with slider
- View detailed trade history table

#### 📊 **Candlestick Charts Tab**
- Enter coin symbol
- Select timeframe (1m to 1d)
- Adjust number of candles
- Interactive zoom and pan

#### 📋 **Order Book Tab**
- Enter coin symbol
- View live bid/ask depth
- Visual order book representation

#### 💰 **Funding Rates Tab**
- Optional coin symbol input
- View all funding rates or specific symbol
- Real-time rate updates

## 🛠️ Development

### Local Setup
```bash
# Clone the repository
git clone https://huggingface.co/spaces/rzvn/hyperliquid-mcp-server
cd hyperliquid-mcp-server

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

### Access Points
- **Gradio Dashboard**: http://localhost:7860
- **MCP API**: http://localhost:3001

### Docker Build
```bash
docker build -t hyperliquid-mcp .
docker run -p 7860:7860 -p 3001:3001 hyperliquid-mcp
```

## 🔗 MCP Integration

This server follows the **Model Context Protocol (MCP)** standard, making it compatible with:
- Claude Desktop
- Cursor AI
- Any MCP-compatible client
- Custom applications

## 📈 Data Coverage

- **200+ Trading Pairs**: All major cryptocurrencies and altcoins
- **Real-time Data**: Live prices, trades, and order books
- **Historical Data**: Candlestick charts with multiple timeframes
- **Perpetual Contracts**: Funding rates and open interest
- **Account Analytics**: Portfolio tracking and position management

## 🎯 Use Cases

### For Traders
- **Real-time market monitoring**
- **Technical analysis with charts**
- **Order book analysis**
- **Funding rate tracking**

### For Developers
- **MCP server integration**
- **RESTful API access**
- **Real-time data feeds**
- **Trading bot development**

### For Analysts
- **Market research**
- **Historical data analysis**
- **Trading strategy backtesting**
- **Market sentiment analysis**

## 🤝 Contributing

Feel free to open issues or submit pull requests to enhance the server with additional Hyperliquid endpoints or features.

## 📄 License

MIT License - Feel free to use this server for your own projects and applications.

---

**Built with ❤️ for the Hyperliquid trading community**

## Last Updated
Tue Jul 15 05:09:24 PM IDT 2025
# Force rebuild Tue Jul 15 05:26:32 PM IDT 2025
