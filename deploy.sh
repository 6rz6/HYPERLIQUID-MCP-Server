#!/bin/bash

# Hyperliquid MCP Server Deployment Script
# This script helps deploy to Hugging Face Spaces

set -e

echo "🚀 Deploying Hyperliquid MCP Server to Hugging Face Spaces..."

# Check if huggingface-cli is installed
if ! command -v huggingface-cli &> /dev/null; then
    echo "❌ huggingface-cli not found. Installing..."
    pip install huggingface_hub
fi

# Check if user is logged in
if ! huggingface-cli whoami &> /dev/null; then
    echo "🔑 Please login to Hugging Face:"
    huggingface-cli login
fi

# Get username
USERNAME=$(huggingface-cli whoami | head -n1)
SPACE_NAME="hyperliquid-mcp-server"

echo "📋 Creating Hugging Face Space: $USERNAME/$SPACE_NAME"

# Create space if it doesn't exist
if ! huggingface-cli repo info $USERNAME/$SPACE_NAME &> /dev/null; then
    echo "🆕 Creating new space..."
    huggingface-cli repo create $SPACE_NAME --repo-type space --space_sdk docker --exist-ok
else
    echo "✅ Space already exists, updating..."
fi

# Clone or update the space
if [ -d "hf-space" ]; then
    echo "📥 Updating existing space..."
    cd hf-space
    git pull
else
    echo "📥 Cloning space..."
    git clone https://huggingface.co/spaces/$USERNAME/$SPACE_NAME hf-space
    cd hf-space
fi

# Copy files
echo "📂 Copying files..."
cp -f ../app.py .
cp -f ../requirements.txt .
cp -f ../Dockerfile .
cp -f ../README.md .
cp -f ../.dockerignore .

# Commit and push
echo "📤 Pushing to Hugging Face..."
git add .
git commit -m "Update Hyperliquid MCP server" || echo "No changes to commit"
git push

echo "✅ Deployment complete!"
echo "🌐 Your space is available at: https://huggingface.co/spaces/$USERNAME/$SPACE_NAME"
echo ""
echo "🔧 Test your deployment:"
echo "curl https://$USERNAME-$SPACE_NAME.hf.space/health"
echo "curl -X POST https://$USERNAME-$SPACE_NAME.hf.space/mcp/tools"