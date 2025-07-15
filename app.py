import json
import requests
import gradio as gr
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import threading

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

# UI helper functions
def get_all_prices_ui():
    """UI function for getting all market prices"""
    result = get_all_mids()
    if result["success"]:
        data = result["data"]
        if data:
            df = pd.DataFrame(list(data.items()), columns=["Symbol", "Price"])
            return df
    return pd.DataFrame()

def get_recent_trades_ui(coin, n):
    """UI function for getting recent trades"""
    result = get_recent_trades(coin.upper(), int(n))
    if result["success"]:
        trades = result["data"]
        if trades:
            df = pd.DataFrame(trades)
            return df, f"✅ Found {len(trades)} trades for {coin.upper()}"
    return pd.DataFrame(), f"❌ No trades found for {coin.upper()}"

def get_candles_ui(coin, interval, limit):
    """UI function for getting candlestick data"""
    result = get_candles(coin.upper(), interval, int(limit))
    if result["success"]:
        candles = result["data"]
        if candles:
            df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            
            fig = go.Figure(data=[go.Candlestick(
                x=df["timestamp"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name=f"{coin.upper()} {interval}"
            )])
            
            fig.update_layout(
                title=f"{coin.upper()} Candlestick Chart ({interval})",
                xaxis_title="Time",
                yaxis_title="Price",
                template="plotly_white"
            )
            
            return fig, f"✅ Loaded {len(df)} candles for {coin.upper()}"
    return go.Figure(), f"❌ No data found for {coin.upper()}"

def get_orderbook_ui(coin):
    """UI function for getting order book"""
    result = get_l2_snapshot(coin.upper())
    if result["success"]:
        data = result["data"]
        if data and "levels" in data:
            levels = data["levels"]
            
            # Process bids and asks
            bids = levels[0] if len(levels) > 0 else []
            asks = levels[1] if len(levels) > 1 else []
            
            if bids and asks:
                bids_df = pd.DataFrame(bids, columns=["price", "size"])
                asks_df = pd.DataFrame(asks, columns=["price", "size"])
                
                fig = go.Figure()
                
                # Bids (green)
                fig.add_trace(go.Bar(
                    x=bids_df["price"],
                    y=bids_df["size"],
                    name="Bids",
                    marker_color="green",
                    opacity=0.7
                ))
                
                # Asks (red)
                fig.add_trace(go.Bar(
                    x=asks_df["price"],
                    y=asks_df["size"],
                    name="Asks",
                    marker_color="red",
                    opacity=0.7
                ))
                
                fig.update_layout(
                    title=f"{coin.upper()} Order Book",
                    xaxis_title="Price",
                    yaxis_title="Size",
                    template="plotly_white"
                )
                
                return fig, f"✅ Loaded order book for {coin.upper()}"
    return go.Figure(), f"❌ No order book data for {coin.upper()}"

def get_funding_rates_ui(coin):
    """UI function for getting funding rates"""
    result = get_funding_rates(coin.upper() if coin else None)
    if result["success"]:
        rates = result["data"]
        if rates:
            df = pd.DataFrame(rates)
            return df
    return pd.DataFrame()

# Create Gradio interface
def create_gradio_interface():
    with gr.Blocks(title="Hyperliquid Trading Dashboard", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 📊 Hyperliquid Trading Dashboard")
        gr.Markdown("Real-time trading data from Hyperliquid decentralized exchange")
        
        with gr.Tab("📈 Market Prices"):
            with gr.Row():
                get_prices_btn = gr.Button("Get All Market Prices", variant="primary")
            prices_output = gr.Dataframe(headers=["Symbol", "Price"], interactive=False)
            get_prices_btn.click(get_all_prices_ui, outputs=prices_output)
        
        with gr.Tab("💱 Recent Trades"):
            with gr.Row():
                coin_input = gr.Textbox(label="Coin Symbol", placeholder="BTC")
                num_trades = gr.Slider(1, 1000, 50, label="Number of Trades")
                get_trades_btn = gr.Button("Get Trades", variant="primary")
            trades_output = gr.Dataframe(interactive=False)
            trades_status = gr.Textbox(label="Status", interactive=False)
            get_trades_btn.click(
                get_recent_trades_ui,
                inputs=[coin_input, num_trades],
                outputs=[trades_output, trades_status]
            )
        
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
        
        # Add MCP API endpoints as hidden tabs
        with gr.Tab("🔧 MCP API"):
            gr.Markdown("## MCP Server API Endpoints")
            gr.Markdown("""
            This dashboard also provides MCP (Model Context Protocol) endpoints:
            
            - **Health Check**: `/health`
            - **List Tools**: `/mcp/tools`
            - **Call Tool**: `/mcp/call`
            
            Use these endpoints to integrate with AI assistants and automated trading systems.
            """)
    
    return demo

# Create the Gradio interface
demo = create_gradio_interface()

# Create Flask app for MCP API endpoints
app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "hyperliquid-mcp-server"})

@app.route('/mcp/tools', methods=['GET'])
def list_tools():
    """List all available MCP tools"""
    return jsonify({"tools": TOOLS})

@app.route('/mcp/call', methods=['POST'])
def call_tool():
    """Execute an MCP tool"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        tool_name = data.get('tool')
        arguments = data.get('arguments', {})
        
        if not tool_name:
            return jsonify({"error": "Tool name is required"}), 400
        
        # Map tool names to functions
        tool_functions = {
            "get_all_mids": get_all_mids,
            "get_user_state": lambda: get_user_state(arguments.get("address")),
            "get_recent_trades": lambda: get_recent_trades(
                arguments.get("coin"),
                arguments.get("n", 100)
            ),
            "get_l2_snapshot": lambda: get_l2_snapshot(arguments.get("coin")),
            "get_candles": lambda: get_candles(
                arguments.get("coin"),
                arguments.get("interval", "1h"),
                arguments.get("limit", 500)
            ),
            "get_meta": get_meta,
            "get_funding_rates": lambda: get_funding_rates(arguments.get("coin")),
            "get_open_interest": lambda: get_open_interest(arguments.get("coin"))
        }
        
        if tool_name not in tool_functions:
            return jsonify({"error": f"Unknown tool: {tool_name}"}), 400
        
        # Execute the tool
        result = tool_functions[tool_name]()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add MCP endpoints using Gradio's FastAPI app
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Add MCP endpoints to Gradio's FastAPI app
@demo.app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "hyperliquid-mcp-server"}

@demo.app.get("/mcp/tools")
async def list_tools():
    """List all available MCP tools"""
    return {"tools": TOOLS}

@demo.app.post("/mcp/call")
async def call_tool(request_data: dict):
    """Execute an MCP tool"""
    try:
        tool_name = request_data.get('tool')
        arguments = request_data.get('arguments', {})
        
        if not tool_name:
            return JSONResponse({"error": "Tool name is required"}, status_code=400)
        
        # Map tool names to functions
        tool_functions = {
            "get_all_mids": get_all_mids,
            "get_user_state": lambda: get_user_state(arguments.get("address")),
            "get_recent_trades": lambda: get_recent_trades(
                arguments.get("coin"),
                arguments.get("n", 100)
            ),
            "get_l2_snapshot": lambda: get_l2_snapshot(arguments.get("coin")),
            "get_candles": lambda: get_candles(
                arguments.get("coin"),
                arguments.get("interval", "1h"),
                arguments.get("limit", 500)
            ),
            "get_meta": get_meta,
            "get_funding_rates": lambda: get_funding_rates(arguments.get("coin")),
            "get_open_interest": lambda: get_open_interest(arguments.get("coin"))
        }
        
        if tool_name not in tool_functions:
            return JSONResponse({"error": f"Unknown tool: {tool_name}"}, status_code=400)
        
        # Execute the tool
        result = tool_functions[tool_name]()
        return result
        
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# Launch Gradio with MCP API endpoints
if __name__ == '__main__':
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        quiet=False,
        show_error=True,
        debug=False
    )