#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import axios from 'axios';
import WebSocket from 'ws';

// Hyperliquid API endpoints
const HYPERLIQUID_API_BASE = 'https://api.hyperliquid.xyz';
const HYPERLIQUID_WS_BASE = 'wss://api.hyperliquid.xyz/ws';

// Create axios instance for Hyperliquid API
const hyperliquidApi = axios.create({
  baseURL: HYPERLIQUID_API_BASE,
  timeout: 30000,
});

// Types for Hyperliquid API responses
interface MarketData {
  coin: string;
  px: string;
  sz: string;
  n: number;
  t: number;
}

interface AllMids {
  [coin: string]: string;
}

interface UserState {
  assetPositions: Array<{
    position: {
      coin: string;
      entryPx: string;
      leverage: string;
      liquidationPx: string;
      marginUsed: string;
      maxLeverage: string;
      positionValue: string;
      returnOnEquity: string;
      szi: string;
      unrealizedPnl: string;
    };
  }>;
  crossMarginSummary: {
    accountValue: string;
    totalMarginUsed: string;
    totalNtlPos: string;
    totalRawUsd: string;
  };
}

interface Candle {
  t: number;
  c: string;
  h: string;
  l: string;
  n: string;
  o: string;
  s: string;
  v: string;
}

interface OrderBook {
  levels: Array<{
    px: string;
    sz: string;
  }>[];
}

// Create MCP server
const server = new McpServer({
  name: "hyperliquid-mcp-server",
  version: "1.0.0"
});

// Helper function to make API calls
async function makeHyperliquidRequest(endpoint: string, data: any) {
  try {
    const response = await hyperliquidApi.post(endpoint, data);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(`Hyperliquid API error: ${error.response?.data?.error || error.message}`);
    }
    throw error;
  }
}

// Tool: Get all market prices
server.tool(
  "get_all_mids",
  {},
  async () => {
    try {
      const data = await makeHyperliquidRequest('/info', {
        type: 'allMids'
      });
      
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(data, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// Tool: Get user state
server.tool(
  "get_user_state",
  {
    user_address: z.string().describe("User's wallet address"),
  },
  async ({ user_address }) => {
    try {
      const data = await makeHyperliquidRequest('/info', {
        type: 'userState',
        user: user_address
      });
      
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(data, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// Tool: Get recent trades
server.tool(
  "get_recent_trades",
  {
    coin: z.string().describe("Trading pair symbol (e.g., 'BTC', 'ETH')"),
    n: z.number().min(1).max(1000).optional().describe("Number of trades to fetch (1-1000, default: 100)"),
  },
  async ({ coin, n = 100 }) => {
    try {
      const data = await makeHyperliquidRequest('/info', {
        type: 'trades',
        coin: coin,
        n: Math.min(n, 1000)
      });
      
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(data, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// Tool: Get order book
server.tool(
  "get_l2_snapshot",
  {
    coin: z.string().describe("Trading pair symbol (e.g., 'BTC', 'ETH')"),
  },
  async ({ coin }) => {
    try {
      const data = await makeHyperliquidRequest('/info', {
        type: 'l2Book',
        coin: coin
      });
      
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(data, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// Tool: Get candle data
server.tool(
  "get_candles",
  {
    coin: z.string().describe("Trading pair symbol (e.g., 'BTC', 'ETH')"),
    interval: z.enum(['1m', '5m', '15m', '1h', '4h', '1d']).describe("Candle interval"),
    start_time: z.number().optional().describe("Start timestamp (milliseconds)"),
    end_time: z.number().optional().describe("End timestamp (milliseconds)"),
    limit: z.number().min(1).max(5000).optional().describe("Number of candles (1-5000, default: 500)"),
  },
  async ({ coin, interval, start_time, end_time, limit = 500 }) => {
    try {
      const requestData: any = {
        type: 'candles',
        coin: coin,
        interval: interval,
        limit: Math.min(limit, 5000)
      };
      
      if (start_time) requestData.startTime = start_time;
      if (end_time) requestData.endTime = end_time;
      
      const data = await makeHyperliquidRequest('/info', requestData);
      
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(data, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// Tool: Get meta information
server.tool(
  "get_meta",
  {},
  async () => {
    try {
      const data = await makeHyperliquidRequest('/info', {
        type: 'meta'
      });
      
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(data, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// Tool: Get funding rates
server.tool(
  "get_funding_rates",
  {
    coin: z.string().optional().describe("Trading pair symbol (optional, returns all if not provided)"),
  },
  async ({ coin }) => {
    try {
      const data = await makeHyperliquidRequest('/info', {
        type: 'fundingRate',
        ...(coin && { coin })
      });
      
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(data, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// Tool: Get open interest
server.tool(
  "get_open_interest",
  {
    coin: z.string().optional().describe("Trading pair symbol (optional, returns all if not provided)"),
  },
  async ({ coin }) => {
    try {
      const data = await makeHyperliquidRequest('/info', {
        type: 'openInterest',
        ...(coin && { coin })
      });
      
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(data, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Hyperliquid MCP server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});