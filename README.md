---
title: Hyperliquid MCP Server
emoji: 📊
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# 🚀 Hyperliquid MCP Server

A production-ready **Model Context Protocol (MCP)** server providing real-time trading data from **Hyperliquid** - the leading decentralized perpetual exchange. Deployed on Hugging Face Spaces for instant access and scalability.

## 🌐 Live Demo
**URL**: https://huggingface.co/spaces/rzvn/hyperliquid-mcp-server

## 📊 Available Trading Tools

### 1. **get_all_mids**
Get real-time market prices for all trading pairs
- **Usage**: No parameters required
- **Returns**: Complete price feed for 200+ trading pairs

### 2. **get_user_state**
Get user account state and positions
- **Parameters**: `address` (string) - User wallet address
- **Returns**: Account balance, positions, and margin information

### 3. **get_recent_trades**
Get recent trades for a specific coin
- **Parameters**: 
  - `coin` (string) - Trading pair symbol (e.g., "BTC", "ETH")
  - `n` (number, optional) - Number of trades (1-1000, default: 100)
- **Returns**: Recent trade history with price, size, and timestamp

### 4. **get_l2_snapshot**
Get L2 order book snapshot
- **Parameters**: `coin` (string) - Trading pair symbol
- **Returns**: Complete order book with bids and asks

### 5. **get_candles**
Get historical candlestick data
- **Parameters**:
  - `coin` (string) - Trading pair symbol
  - `interval` (string, optional) - Time interval ("1m", "5m", "1h", "1d")
  - `limit` (number, optional) - Number of candles (1-5000, default: 500)
  - `startTime` (number, optional) - Start timestamp (ms)
  - `endTime` (number, optional) - End timestamp (ms)
- **Returns**: OHLCV candlestick data

### 6. **get_meta**
Get market metadata
- **Usage**: No parameters required
- **Returns**: Market specifications, asset details, and trading parameters

### 7. **get_funding_rates**
Get funding rates for perpetual contracts
- **Parameters**: `coin` (string, optional) - Specific trading pair or all
- **Returns**: Current funding rates for perpetual contracts

### 8. **get_open_interest**
Get open interest data
- **Parameters**: `coin` (string) - Trading pair symbol
- **Returns**: Current open interest across all markets

## 🔧 API Usage

### Base URL
```
https://rzvn-hyperliquid-mcp-server.hf.space
```

### Endpoints
- **Health Check**: `GET /health`
- **List Tools**: `POST /mcp/tools`
- **Execute Tool**: `POST /mcp/call`

### Example Usage

#### 1. Health Check
```bash
curl https://rzvn-hyperliquid-mcp-server.hf.space/health
```

#### 2. List All Available Tools
```bash
curl -X POST https://rzvn-hyperliquid-mcp-server.hf.space/mcp/tools \
  -H "Content-Type: application/json"
```

#### 3. Get All Market Prices
```bash
curl -X POST https://rzvn-hyperliquid-mcp-server.hf.space/mcp/call \
  -H "Content-Type: application/json" \
  -d '{"name": "get_all_mids", "arguments": {}}'
```

#### 4. Get Recent BTC Trades
```bash
curl -X POST https://rzvn-hyperliquid-mcp-server.hf.space/mcp/call \
  -H "Content-Type: application/json" \
  -d '{"name": "get_recent_trades", "arguments": {"coin": "BTC", "n": 50}}'
```

#### 5. Get ETH Candlestick Data
```bash
curl -X POST https://rzvn-hyperliquid-mcp-server.hf.space/mcp/call \
  -H "Content-Type: application/json" \
  -d '{"name": "get_candles", "arguments": {"coin": "ETH", "interval": "1h", "limit": 100}}'
```

#### 6. Get User Account State
```bash
curl -X POST https://rzvn-hyperliquid-mcp-server.hf.space/mcp/call \
  -H "Content-Type: application/json" \
  -d '{"name": "get_user_state", "arguments": {"address": "0x1234...abcd"}}'
```

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

### Docker Build
```bash
docker build -t hyperliquid-mcp .
docker run -p 7860:7860 hyperliquid-mcp
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

- **Trading Bots**: Real-time price feeds and order book data
- **Portfolio Trackers**: Account state and position monitoring
- **Analytics Platforms**: Historical data and market insights
- **DeFi Applications**: Perpetual contract data integration
- **AI Assistants**: Market data for trading decisions

## 🤝 Contributing

Feel free to open issues or submit pull requests to enhance the server with additional Hyperliquid endpoints or features.

## 📄 License

MIT License - Feel free to use this server for your own projects and applications.

---

**Built by rz with ❤️ for the Hyperliquid trading community**