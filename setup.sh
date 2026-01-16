#!/bin/bash

# MCP Server Setup Script for Unraid
# Author: Cooley McCoolson
# Created: 2026-01-16

set -e

UNRAID_HOST="root@${UNRAID_IP:-10.27.27.157}"
MCP_PATH="/mnt/cache_nvme/appdata/mcp"

echo "================================"
echo "MCP Server Setup for Unraid"
echo "================================"
echo ""

# Check if connected to Unraid
echo "Checking connection to Unraid..."
ssh -o ConnectTimeout=5 "$UNRAID_HOST" "hostname" || {
    echo "❌ Cannot connect to Unraid at $UNRAID_HOST"
    echo "Please ensure:"
    echo "  - Unraid is reachable"
    echo "  - SSH key is configured"
    echo "  - You can run: ssh $UNRAID_HOST"
    exit 1
}

echo "✅ Connected to $(ssh $UNRAID_HOST hostname)"
echo ""

# Create directory structure
echo "Creating directory structure on Unraid..."
ssh "$UNRAID_HOST" "mkdir -p $MCP_PATH/{brave-search,sequential-thinking,fetch-content,obsidian}"
echo "✅ Directories created"
echo ""

# Copy files to Unraid
echo "Copying project files to Unraid..."
scp docker-compose.yml "$UNRAID_HOST:$MCP_PATH/"
scp .env "$UNRAID_HOST:$MCP_PATH/" 2>/dev/null || echo "⚠️  .env not found, using .env.example"
scp .env.example "$UNRAID_HOST:$MCP_PATH/"
echo "✅ Files copied"
echo ""

# Instructions
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo ""
echo "1. SSH into Unraid:"
echo "   ssh $UNRAID_HOST"
echo ""
echo "2. Navigate to MCP directory:"
echo "   cd $MCP_PATH"
echo ""
echo "3. Configure environment:"
echo "   cp .env.example .env"
echo "   nano .env  # Add your Brave API key"
echo ""
echo "4. Start services:"
echo "   docker-compose up -d"
echo ""
echo "5. Verify services are running:"
echo "   docker ps | grep mcp"
echo ""
echo "6. View logs:"
echo "   docker-compose logs -f"
echo ""
echo "============================================================"
echo "Once running, configure Claude Code to use these endpoints:"
echo "============================================================"
echo ""
echo "Brave Search:    http://\${UNRAID_IP:-10.27.27.157}:8011/mcp"
echo ""
