# HYPERLIQUID-MCP-Server

A Model Context Protocol (MCP) server for interacting with the Hyperliquid trading platform. This server provides comprehensive tools to access market data, trading information, user positions, and analytics for the Hyperliquid perpetual futures exchange.

## Features

- **Real-time Market Data**: Get live prices, order books, and trading volumes
- **Trading Analytics**: Access candlestick data, funding rates, and open interest
- **Account Management**: Query user positions, balances, and trading history
- **Market Intelligence**: Get meta information about all available trading pairs
- **WebSocket Support**: Real-time data streaming capabilities
- **Comprehensive Coverage**: All major Hyperliquid endpoints supported

## Installation

```bash
git clone https://github.com/6rz6/HYPERLIQUID-MCP-Server.git
cd HYPERLIQUID-MCP-Server
npm install
npm run build
```

## Usage

### MCP Configuration

Add to your MCP settings:

```json
{
  "mcpServers": {
    "hyperliquid": {
      "command": "node",
      "args": ["/path/to/HYPERLIQUID-MCP-Server/build/index.js"]
    }
  }
}
```

### Available Tools

1. **get_all_mids** - Get all current market prices
2. **get_user_state** - Get user account information and positions
3. **get_recent_trades** - Get recent trading activity
4. **get_l2_snapshot** - Get order book depth
5. **get_candles** - Get historical candlestick data
6. **get_meta** - Get market metadata and available pairs
7. **get_funding_rates** - Get funding rates for perpetuals
8. **get_open_interest** - Get open interest data

### Examples

```bash
# Get all market prices
get_all_mids()

# Get user positions (replace with actual address)
get_user_state("0x1234567890abcdef1234567890abcdef12345678")

# Get recent BTC trades
get_recent_trades("BTC", 50)

# Get ETH order book
get_l2_snapshot("ETH")

# Get 1-hour candles for BTC
get_candles("BTC", "1h", 100)

# Get market metadata
get_meta()

# Get funding rates
get_funding_rates("BTC")

# Get open interest
get_open_interest("ETH")
```

## API Reference

### Market Data Tools

#### get_all_mids()
Returns current mid prices for all trading pairs.

**Response:**
```json
{
  "BTC": "43250.5",
  "ETH": "2650.25",
  "SOL": "98.75"
}
```

#### get_recent_trades(coin, n)
Returns recent trades for a specific trading pair.

**Parameters:**
- `coin` (string): Trading pair symbol (e.g., "BTC", "ETH")
- `n` (number, optional): Number of trades to fetch (1-1000, default: 100)

#### get_l2_snapshot(coin)
Returns Level 2 order book snapshot.

**Parameters:**
- `coin` (string): Trading pair symbol

#### get_candles(coin, interval, limit, start_time, end_time)
Returns historical candlestick data.

**Parameters:**
- `coin` (string): Trading pair symbol
- `interval` (string): Candle interval ("1m", "5m", "15m", "1h", "4h", "1d")
- `limit` (number, optional): Number of candles (1-5000, default: 500)
- `start_time` (number, optional): Start timestamp in milliseconds
- `end_time` (number, optional): End timestamp in milliseconds

### Account Tools

#### get_user_state(user_address)
Returns user account information including positions and balances.

**Parameters:**
- `user_address` (string): User's wallet address

**Response:**
```json
{
  "assetPositions": [...],
  "crossMarginSummary": {
    "accountValue": "10000.50",
    "totalMarginUsed": "2500.25",
    "totalNtlPos": "5000.00",
    "totalRawUsd": "10000.50"
  }
}
```

### Market Information Tools

#### get_meta()
Returns metadata about all available trading pairs.

#### get_funding_rates(coin)
Returns funding rates for perpetual contracts.

**Parameters:**
- `coin` (string, optional): Specific trading pair (returns all if omitted)

#### get_open_interest(coin)
Returns open interest data.

**Parameters:**
- `coin` (string, optional): Specific trading pair (returns all if omitted)

## Development

```bash
# Watch mode
npm run dev

# Build TypeScript
npm run build

# Start server
npm start
```

## Environment Variables

No API keys required - Hyperliquid's public API is open access.

## License

MIT