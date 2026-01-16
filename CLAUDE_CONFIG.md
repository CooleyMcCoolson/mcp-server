# Claude Code MCP Bridge Configuration

## Overview

Use the bridge script to connect Claude Code to your centralized Unraid MCP servers.

## Setup

### Step 1: Copy the bridge script to each machine

```bash
# On each of your 4 machines
mkdir -p ~/.local/bin
cp mcp-bridge.py ~/.local/bin/
chmod +x ~/.local/bin/mcp-bridge.py
```

### Step 2: Configure Claude Code

Edit `~/.claude/settings.local.json` and add the MCP server configuration:

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "python3",
      "args": ["~/.local/bin/mcp-bridge.py", "http://${UNRAID_IP}:8011/mcp"]
    }
  }
}
```

### Step 3: Restart Claude Code

Close and reopen Claude Code, or reload the configuration.

## Usage

Once configured, Claude Code can use Brave Search through the centralized Unraid server.

## Architecture

```
┌─────────────────┐     stdio      ┌──────────────┐     HTTP      ┌──────────────┐
│  Claude Code    │◄──────────────►│  mcp-bridge  │◄────────────►│ Unraid MCP   │
│  (local)        │   (localhost)  │  (local)     │   (network)  │  (central)   │
└─────────────────┘                └──────────────┘              └──────────────┘
```

## Benefits

- ✅ Single MCP server to manage
- ✅ One API key configuration
- ✅ Easy updates - just restart the Unraid container
- ✅ All 4 machines share the same service

## Troubleshooting

### Connection Refused
```bash
# Check if Unraid MCP is running
curl http://${UNRAID_IP}:8011/mcp

# Check container status
ssh root@${UNRAID_IP} "docker ps | grep mcp"
```

### Permission Errors
```bash
# Make sure bridge script is executable
chmod +x ~/.local/bin/mcp-bridge.py
```

### Python Not Found
```bash
# Install Python 3
sudo apt install python3  # Ubuntu/Debian
brew install python3      # macOS
```
