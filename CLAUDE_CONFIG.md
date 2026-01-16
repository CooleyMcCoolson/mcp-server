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

### Step 2: Add MCP server using Claude CLI

Use the `claude mcp add` command to properly configure the bridge:

```bash
# Add Brave Search MCP (user scope - available in all projects)
claude mcp add -e PYTHONUNBUFFERED=1 --scope user brave-search -- \
  python3 ~/.local/bin/mcp-bridge.py http://${UNRAID_IP}:8011/mcp
```

**Note:** Replace `${UNRAID_IP}` with your actual Unraid IP address.

### Step 3: Verify the connection

```bash
# List all configured MCP servers
claude mcp list

# Get details for brave-search
claude mcp get brave-search
```

### Step 4: Add tool permissions (optional auto-approve)

Add the Brave Search tools to your `~/.claude/settings.local.json` permissions:

```json
{
  "permissions": {
    "allow": [
      "mcp__brave-search__brave_web_search",
      "mcp__brave-search__brave_local_search",
      "mcp__brave-search__brave_image_search",
      "mcp__brave-search__brave_video_search",
      "mcp__brave-search__brave_news_search",
      "mcp__brave-search__brave_summarizer"
    ]
  }
}
```

## Usage

Once configured, Claude Code can use Brave Search through the centralized Unraid server. The MCP tools will be available in all Claude Code sessions.

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
- ✅ Proper configuration using official `claude mcp` CLI

## Troubleshooting

### Connection Refused
```bash
# Check if Unraid MCP is running
curl http://${UNRAID_IP}:8011/mcp

# Check container status
ssh root@${UNRAID_IP} "docker ps | grep mcp"
```

### MCP Server Not Showing
```bash
# Check MCP server status
claude mcp list

# Re-add the server if needed
claude mcp remove brave-search -s user
claude mcp add -e PYTHONUNBUFFERED=1 --scope user brave-search -- \
  python3 ~/.local/bin/mcp-bridge.py http://${UNRAID_IP}:8011/mcp
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

## MCP CLI Reference

```bash
# List all MCP servers
claude mcp list

# Get details for a specific server
claude mcp get brave-search

# Remove a server
claude mcp remove brave-search -s user

# Check MCP server health (in Claude Code)
/mcp
```

## Configuration Scopes

- **User scope** (`--scope user`): Available across all projects (recommended for shared services)
- **Local scope** (default): Only available in current project directory
- **Project scope** (`--scope project`): Shared with team via `.mcp.json` in git

For centralized Unraid services, use `--scope user` so the service is available everywhere.
