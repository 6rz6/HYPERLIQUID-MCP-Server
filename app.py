#!/usr/bin/env python3
"""
Hyperliquid MCP Server - Pure MCP Implementation
Provides 8 trading tools for Hyperliquid DEX via MCP protocol
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
import aiohttp
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Hyperliquid MCP Server",
    description="MCP server providing 8 trading tools for Hyperliquid DEX",
    version="1.0.0"
)

# Constants
HYPERLIQUID_API_BASE = "https://api.hyperliquid.xyz/info"

# Pydantic models
class ToolCallRequest(BaseModel):
    name: str
    arguments: Dict[str, Any] = {}

class ToolCallResponse(BaseModel):
    content: List[Dict[str, Any]]
    isError: bool = False

# MCP Tools Definition
MCP_TOOLS = [
    {
        "name": "get_all_mids",
        "description": "Get all market IDs (symbols) available on Hyperliquid",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_user_state",
        "description": "Get user account state including balances and positions",
        "inputSchema": {
            "type": "object",
            "properties": {
                "user_address": {
                    "type": "string",
                    "description": "User wallet address"
                }
            },
            "required": ["user_address"]
        }
    },
    {
        "name": "get_recent_trades",
        "description": "Get recent trades for a specific coin",
        "inputSchema": {
            "type": "object",
            "properties": {
                "coin": {
                    "type": "string",
                    "description": "Coin symbol (e.g., 'BTC', 'ETH')"
                },
                "n": {
                    "type": "number",
                    "description": "Number of trades to return (default: 100)",
                    "default": 100
                }
            },
            "required": ["coin"]
        }
    },
    {
        "name": "get_l2_snapshot",
        "description": "Get Level 2 order book snapshot for a coin",
        "inputSchema": {
            "type": "object",
            "properties": {
                "coin": {
                    "type": "string",
                    "description": "Coin symbol"
                }
            },
            "required": ["coin"]
        }
    },
    {
        "name": "get_candles",
        "description": "Get OHLCV candlestick data for a coin",
        "inputSchema": {
            "type": "object",
            "properties": {
                "coin": {
                    "type": "string",
                    "description": "Coin symbol"
                },
                "interval": {
                    "type": "string",
                    "description": "Candle interval (e.g., '1m', '5m', '1h', '1d')",
                    "default": "1h"
                },
                "start_time": {
                    "type": "number",
                    "description": "Start timestamp (milliseconds)"
                },
                "end_time": {
                    "type": "number",
                    "description": "End timestamp (milliseconds)"
                }
            },
            "required": ["coin"]
        }
    },
    {
        "name": "get_meta",
        "description": "Get exchange metadata including asset information",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_funding_rates",
        "description": "Get current funding rates for all perpetual markets",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_open_interest",
        "description": "Get open interest data for all markets",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

# API Helper Functions
async def make_hyperliquid_request(endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Make a request to the Hyperliquid API"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{HYPERLIQUID_API_BASE}/{endpoint}",
                json=payload,
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Hyperliquid API error: {response.status}"
                    )
        except Exception as e:
            logger.error(f"Error making request to Hyperliquid: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
# Tool Implementations
async def get_all_mids() -> Dict[str, Any]:
    """Get all market IDs"""
    try:
        result = await make_hyperliquid_request("allMids", {})
        return {"mids": result}
    except Exception as e:
        return {"error": str(e)}

async def get_user_state(user_address: str) -> Dict[str, Any]:
    """Get user account state"""
    try:
        payload = {"type": "clearinghouseState", "user": user_address}
        result = await make_hyperliquid_request("", payload)
        return {"user_state": result}
    except Exception as e:
        return {"error": str(e)}

async def get_recent_trades(coin: str, n: int = 100) -> Dict[str, Any]:
    """Get recent trades for a coin"""
    try:
        payload = {"type": "trades", "coin": coin, "n": n}
        result = await make_hyperliquid_request("", payload)
        return {"trades": result}
    except Exception as e:
        return {"error": str(e)}

async def get_l2_snapshot(coin: str) -> Dict[str, Any]:
    """Get Level 2 order book snapshot"""
    try:
        payload = {"type": "l2Book", "coin": coin}
        result = await make_hyperliquid_request("", payload)
        return {"l2_snapshot": result}
    except Exception as e:
        return {"error": str(e)}

async def get_candles(coin: str, interval: str = "1h", start_time: Optional[int] = None, end_time: Optional[int] = None) -> Dict[str, Any]:
    """Get candlestick data"""
    try:
        payload = {
            "type": "candles",
            "coin": coin,
            "interval": interval,
        }
        if start_time:
            payload["startTime"] = start_time
        if end_time:
            payload["endTime"] = end_time
            
        result = await make_hyperliquid_request("", payload)
        return {"candles": result}
    except Exception as e:
        return {"error": str(e)}

async def get_meta() -> Dict[str, Any]:
    """Get exchange metadata"""
    try:
        payload = {"type": "meta"}
        result = await make_hyperliquid_request("", payload)
        return {"meta": result}
    except Exception as e:
        return {"error": str(e)}

async def get_funding_rates() -> Dict[str, Any]:
    """Get funding rates"""
    try:
        payload = {"type": "fundingRates"}
        result = await make_hyperliquid_request("", payload)
        return {"funding_rates": result}
    except Exception as e:
        return {"error": str(e)}

async def get_open_interest() -> Dict[str, Any]:
    """Get open interest data"""
    try:
        payload = {"type": "openInterest"}
        result = await make_hyperliquid_request("", payload)
        return {"open_interest": result}
    except Exception as e:
        return {"error": str(e)}

# Tool execution router
async def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a specific tool based on name and arguments"""
    tool_map = {
        "get_all_mids": get_all_mids,
        "get_user_state": lambda: get_user_state(arguments.get("user_address", "")),
        "get_recent_trades": lambda: get_recent_trades(
            arguments.get("coin", ""),
            arguments.get("n", 100)
        ),
        "get_l2_snapshot": lambda: get_l2_snapshot(arguments.get("coin", "")),
        "get_candles": lambda: get_candles(
            arguments.get("coin", ""),
            arguments.get("interval", "1h"),
            arguments.get("start_time"),
            arguments.get("end_time")
        ),
        "get_meta": get_meta,
        "get_funding_rates": get_funding_rates,
        "get_open_interest": get_open_interest
    }
    
    if tool_name not in tool_map:
        return {"error": f"Unknown tool: {tool_name}"}
    
    try:
        if tool_name in ["get_user_state", "get_recent_trades", "get_l2_snapshot", "get_candles"]:
            return await tool_map[tool_name]()
        else:
            return await tool_map[tool_name]()
    except Exception as e:
        return {"error": str(e)}

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Hyperliquid MCP Server",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "tools": "/mcp/tools",
            "call": "/mcp/call"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/mcp/tools")
async def list_tools():
    """List all available MCP tools"""
    return {"tools": MCP_TOOLS}

@app.post("/mcp/call")
async def call_tool(request: ToolCallRequest):
    """Execute a specific MCP tool"""
    try:
        result = await execute_tool(request.name, request.arguments)
        
        # Format response according to MCP protocol
        content = []
        if "error" in result:
            content.append({
                "type": "text",
                "text": f"Error: {result['error']}"
            })
            return ToolCallResponse(content=content, isError=True)
        else:
            content.append({
                "type": "text",
                "text": json.dumps(result, indent=2, default=str)
            })
            return ToolCallResponse(content=content)
    
    except Exception as e:
        return ToolCallResponse(
            content=[{"type": "text", "text": f"Error: {str(e)}"}],
            isError=True
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
