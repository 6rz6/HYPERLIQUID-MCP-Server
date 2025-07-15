import json
import requests
import gradio as gr
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Hyperliquid API base URL
HYPERLIQUID_API = "https://api.hyperliquid.xyz/info"

# Tool definitions
TOOLS = [
    {
        "name": "get_all_mids",
        "description": "Get all market prices from Hyperliquid",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "get_user_state",
        "description": "Get user account state and positions",
        "inputSchema": {
            "type": "object",
            "properties": {
                "address": {"type": "string", "description": "User wallet address"}
            },
            "required": ["address"]
        }
    },
    {
        "name": "get_recent_trades",
        "description": "Get recent trades for a specific coin",
        "inputSchema": {
            "type": "object",
            "properties": {
                "coin": {"type": "string", "description": "Trading pair symbol (e.g., 'BTC')"},
                "n": {"type": "number", "description": "Number of trades to retrieve (1-1000)", "default": 100}
            },
            "required": ["coin"]
        }
    },
    {
        "name": "get_l2_snapshot",
        "description": "Get L2 order book snapshot",
        "inputSchema": {
            "type": "object",
            "properties": {
                "coin": {"type": "string", "description": "Trading pair symbol (e.g., 'BTC')"}
            },
            "required": ["coin"]
        }
    },
    {
        "name": "get_candles",
        "description": "Get historical candlestick data",
        "inputSchema": {
            "type": "object",
            "properties": {
                "coin": {"type": "string", "description": "Trading pair symbol (e.g., 'BTC')"},
                "interval": {"type": "string", "description": "Time interval (e.g., '1m', '5m', '1h', '1d')", "default": "1h"},
                "limit": {"type": "number", "description": "Number of candles to retrieve (1-5000)", "default": 500}
            },
            "required": ["coin"]
        }
    },
    {
        "name": "get_meta",
        "description": "Get market metadata",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "get_funding_rates",
        "description": "Get funding rates for perpetual contracts",
        "inputSchema": {
            "type": "object",
            "properties": {
                "coin": {"type": "string", "description": "Trading pair symbol (optional)"}
            }
        }
    },
    {
        "name": "get_open_interest",
        "description": "Get open interest data",
        "inputSchema": {
            "type": "object",
            "properties": {
                "coin": {"type": "string", "description": "Trading pair symbol"}
            },
            "required": ["coin"]
        }
    }
]

# Tool implementations
def get_all_mids():
    """Get all market prices from Hyperliquid"""
    try:
        response = requests.post(HYPERLIQUID_API, json={"type": "allMids"})
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_user_state(address):
    """Get user account state and positions"""
    try:
        response = requests.post(HYPERLIQUID_API, json={
            "type": "userState",
            "user": address
        })
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_recent_trades(coin, n=100):
    """Get recent trades for a specific coin"""
    try:
        response = requests.post(HYPERLIQUID_API, json={
            "type": "trades",
            "coin": coin,
            "n": n
        })
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_l2_snapshot(coin):
    """Get L2 order book snapshot"""
    try:
        response = requests.post(HYPERLIQUID_API, json={
            "type": "l2Book",
            "coin": coin
        })
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_candles(coin, interval="1h", limit=500):
    """Get historical candlestick data"""
    try:
        response = requests.post(HYPERLIQUID_API, json={
            "type": "candles",
            "coin": coin,
            "interval": interval,
            "limit": limit
        })
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_meta():
    """Get market metadata"""
    try:
        response = requests.post(HYPERLIQUID_API, json={"type": "meta"})
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_funding_rates(coin=None):
    """Get funding rates for perpetual contracts"""
    try:
        payload = {"type": "fundingRate"}
        if coin:
            payload["coin"] = coin
        response = requests.post(HYPERLIQUID_API, json=payload)
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_open_interest(coin):
    """Get open interest data"""
    try:
        response = requests.post(HYPERLIQUID_API, json={
            "type": "openInterest",
            "coin": coin
        })
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}

# FastAPI app
app = FastAPI(title="Hyperliquid MCP Server", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: dict = {}

# API endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "hyperliquid-mcp-server"}

@app.get("/mcp/tools")
async def list_tools():
    """List all available MCP tools"""
    return {"tools": TOOLS}

@app.post("/mcp/call")
async def call_tool(request: ToolCallRequest):
    """Execute an MCP tool"""
    try:
        tool_name = request.tool_name
        args = request.arguments
        
        tool_functions = {
            "get_all_mids": get_all_mids,
            "get_user_state": lambda: get_user_state(args.get("address")),
            "get_recent_trades": lambda: get_recent_trades(args.get("coin"), args.get("n", 100)),
            "get_l2_snapshot": lambda: get_l2_snapshot(args.get("coin")),
            "get_candles": lambda: get_candles(args.get("coin"), args.get("interval", "1h"), args.get("limit", 500)),
            "get_meta": get_meta,
            "get_funding_rates": lambda: get_funding_rates(args.get("coin")),
            "get_open_interest": lambda: get_open_interest(args.get("coin"))
        }
        
        if tool_name in tool_functions:
            return tool_functions[tool_name]()
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    except Exception as e:
        return {"error": str(e)}

# Gradio UI functions
def get_all_prices_ui():
    """Get all market prices for UI"""
    result = get_all_mids()
    if result["success"]:
        data = result["data"]
        if isinstance(data, dict):
            df = pd.DataFrame(list(data.items()), columns=["Symbol", "Price"])
            return df
    return pd.DataFrame([["No data available", ""]], columns=["Symbol", "Price"])

def get_recent_trades_ui(coin, n=50):
    """Get recent trades for UI"""
    result = get_recent_trades(coin, n)
    if result["success"]:
        trades = result["data"]
        if trades:
            df = pd.DataFrame(trades)
            return df, f"Loaded {len(trades)} trades for {coin}"
    return pd.DataFrame([["No trades found", "", ""]], columns=["Time", "Price", "Size"]), f"No trades found for {coin}"

def get_candles_ui(coin, interval="1h", limit=100):
    """Get candlestick data for UI"""
    result = get_candles(coin, interval, limit)
    if result["success"]:
        candles = result["data"]
        if candles:
            df = pd.DataFrame(candles, columns=["Time", "Open", "High", "Low", "Close", "Volume"])
            df["Time"] = pd.to_datetime(df["Time"], unit="ms")
            
            fig = go.Figure(data=[go.Candlestick(
                x=df["Time"],
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                name=coin
            )])
            fig.update_layout(
                title=f"{coin} Candlestick Chart ({interval})",
                xaxis_title="Time",
                yaxis_title="Price",
                template="plotly_white"
            )
            return fig, f"Loaded {len(candles)} candles for {coin}"
    return go.Figure(), f"Could not load candles for {coin}"

def get_orderbook_ui(coin):
    """Get order book for UI"""
    result = get_l2_snapshot(coin)
    if result["success"]:
        data = result["data"]
        if data and "levels" in data:
            levels = data["levels"]
            if levels:
                bids = levels[0]
                asks = levels[1]
                
                bid_prices = [float(b[0]) for b in bids]
                bid_sizes = [float(b[1]) for b in bids]
                ask_prices = [float(a[0]) for a in asks]
                ask_sizes = [float(a[1]) for a in asks]
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=bid_prices,
                    y=bid_sizes,
                    name="Bids",
                    marker_color="green",
                    orientation="v"
                ))
                fig.add_trace(go.Bar(
                    x=ask_prices,
                    y=ask_sizes,
                    name="Asks",
                    marker_color="red",
                    orientation="v"
                ))
                fig.update_layout(
                    title=f"{coin} Order Book",
                    xaxis_title="Price",
                    yaxis_title="Size",
                    template="plotly_white"
                )
                return fig, f"Order book loaded for {coin}"
    return go.Figure(), f"Could not load order book for {coin}"

def get_funding_rates_ui(coin=None):
    """Get funding rates for UI"""
    result = get_funding_rates(coin)
    if result["success"]:
        rates = result["data"]
        if rates:
            df = pd.DataFrame(rates)
            return df
    return pd.DataFrame([["No data available", ""]], columns=["Status", "Value"])

# Create Gradio interface
with gr.Blocks(title="Hyperliquid Trading Dashboard") as demo:
    gr.Markdown("# 📊 Hyperliquid Trading Dashboard")
    gr.Markdown("Real-time trading data from Hyperliquid decentralized exchange")
    
    with gr.Tabs():
        # Market Prices Tab
        with gr.Tab("📈 Market Prices"):
            with gr.Row():
                get_all_btn = gr.Button("Get All Market Prices", variant="primary")
            prices_output = gr.Dataframe(interactive=False)
            get_all_btn.click(get_all_prices_ui, outputs=prices_output)
        
        # Recent Trades Tab
        with gr.Tab("💱 Recent Trades"):
            with gr.Row():
                coin_input = gr.Textbox(label="Coin Symbol", placeholder="BTC")
                trades_count = gr.Slider(1, 1000, 50, label="Number of Trades")
                get_trades_btn = gr.Button("Get Trades", variant="primary")
            trades_output = gr.Dataframe(interactive=False)
            trades_status = gr.Textbox(label="Status", interactive=False)
            get_trades_btn.click(
                get_recent_trades_ui,
                inputs=[coin_input, trades_count],
                outputs=[trades_output, trades_status]
            )
        
        # Candlestick Charts Tab
        with gr.Tab("📊 Candlestick Charts"):
            with gr.Row():
                candle_coin = gr.Textbox(label="Coin Symbol", placeholder="BTC")
                candle_interval = gr.Dropdown(
                    choices=["1m", "5m", "15m", "1h", "4h", "1d"],
                    value="1h",
                    label="Interval"
                )
                candle_limit = gr.Slider(10, 1000, 100, label="Number of Candles")
                get_candles_btn = gr.Button("Get Chart", variant="primary")
            candle_chart = gr.Plot()
            candle_status = gr.Textbox(label="Status", interactive=False)
            get_candles_btn.click(
                get_candles_ui,
                inputs=[candle_coin, candle_interval, candle_limit],
                outputs=[candle_chart, candle_status]
            )
        
        # Order Book Tab
        with gr.Tab("📋 Order Book"):
            with gr.Row():
                orderbook_coin = gr.Textbox(label="Coin Symbol", placeholder="BTC")
                get_orderbook_btn = gr.Button("Get Order Book", variant="primary")
            orderbook_chart = gr.Plot()
            orderbook_status = gr.Textbox(label="Status", interactive=False)
            get_orderbook_btn.click(
                get_orderbook_ui,
                inputs=[orderbook_coin],
                outputs=[orderbook_chart, orderbook_status]
            )
        
        # Funding Rates Tab
        with gr.Tab("💰 Funding Rates"):
            with gr.Row():
                funding_coin = gr.Textbox(label="Coin Symbol (optional)", placeholder="BTC")
                get_funding_btn = gr.Button("Get Funding Rates", variant="primary")
            funding_output = gr.Dataframe(interactive=False)
            get_funding_btn.click(
                get_funding_rates_ui,
                inputs=[funding_coin],
                outputs=[funding_output]
            )
        
        # MCP API Tab
        with gr.Tab("🔧 MCP API"):
            gr.Markdown("## MCP Server API Endpoints")
            gr.Markdown("This dashboard provides MCP (Model Context Protocol) endpoints for AI integration:")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Available Tools")
                    tools_display = gr.JSON(value=TOOLS, label="MCP Tools")
                    
                    gr.Markdown("### Test MCP Tools")
                    tool_name = gr.Dropdown(
                        choices=[tool["name"] for tool in TOOLS],
                        label="Select Tool",
                        value="get_all_mids"
                    )
                    arguments = gr.Textbox(
                        label="Arguments (JSON format)",
                        placeholder='{"coin": "BTC"}',
                        value="{}"
                    )
                    call_btn = gr.Button("Call Tool", variant="primary")
                    result_display = gr.JSON(label="Result")
                    
                    call_btn.click(
                        fn=lambda tool, args: call_tool_sync(tool, args),
                        inputs=[tool_name, arguments],
                        outputs=result_display
                    )
                    
                    gr.Markdown("### API Endpoints")
                    gr.Markdown("""
                    - **Health Check**: `GET /health`
                    - **List Tools**: `GET /mcp/tools`
                    - **Call Tool**: `POST /mcp/call`
                    
                    Use these endpoints to integrate with AI assistants and automated trading systems.
                    """)

def call_tool_sync(tool_name, arguments_str):
    """Synchronous wrapper for tool calls"""
    try:
        args = json.loads(arguments_str) if arguments_str else {}
        
        tool_functions = {
            "get_all_mids": get_all_mids,
            "get_user_state": lambda: get_user_state(args.get("address")),
            "get_recent_trades": lambda: get_recent_trades(args.get("coin"), args.get("n", 100)),
            "get_l2_snapshot": lambda: get_l2_snapshot(args.get("coin")),
            "get_candles": lambda: get_candles(args.get("coin"), args.get("interval", "1h"), args.get("limit", 500)),
            "get_meta": get_meta,
            "get_funding_rates": lambda: get_funding_rates(args.get("coin")),
            "get_open_interest": lambda: get_open_interest(args.get("coin"))
        }
        
        if tool_name in tool_functions:
            return tool_functions[tool_name]()
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    except Exception as e:
        return {"error": str(e)}

# Mount Gradio app to FastAPI at /ui path
app = gr.mount_gradio_app(app, demo, path="/ui")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)# Trigger rebuild - Tue Jul 15 04:57:04 PM IDT 2025
