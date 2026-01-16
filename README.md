# MCP Server - Centralized AI Context Services

**Author:** Cooley McCoolson
**Created:** 2026-01-16
**Purpose:** Centralized Model Context Protocol (MCP) servers for multi-machine AI workflow

---

## Overview

This project runs MCP servers on Unraid, providing shared AI context services to 4 machines on the network. All machines running Claude Code or similar AI tools can leverage these centralized services.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Unraid Server                            │
│                  (${UNRAID_IP} / ${UNRAID_HOSTNAME})         │
│                                                               │
│  ┌──────────────┐  ┌───────────────┐  ┌─────────────────┐  │
│  │  Brave       │  │  Sequential   │  │   Fetch         │  │
│  │  Search MCP  │  │  Thinking MCP │  │   Content MCP   │  │
│  └──────────────┘  └───────────────┘  └─────────────────┘  │
│         │                  │                    │            │
└─────────┼──────────────────┼────────────────────┼────────────┘
          │                  │                    │
          └──────────────────┼────────────────────┘
                             │
          ┌──────────────────┼────────────────────┐
          │                  │                    │
     ┌────▼────┐       ┌────▼────┐         ┌────▼────┐
     │ Laptop  │       │ PC #2   │         │ PC #3   │
     │ (primary)│      │         │         │         │
     └─────────┘       └─────────┘         └─────────┘
```

---

## MCP Services

| Service | Purpose | Port | Endpoint |
|---------|---------|------|----------|
| **Brave Search** | Web search via Brave API | 8011 | http://${UNRAID_IP}:8011/mcp |

---

## Setup

### Prerequisites

- Unraid server with Docker
- Brave Search API key
- Obsidian sync server configured
- Port forwarding: 8001-8010 available

### Installation

1. **Create directories on Unraid:**
   ```bash
   ssh root@${UNRAID_IP}
   mkdir -p /mnt/appdata/mcp/{brave-search,sequential-thinking,fetch-content,obsidian}
   ```

2. **Deploy containers:**
   ```bash
   cd /mnt/appdata/mcp
   docker-compose up -d
   ```

3. **Configure Claude Code on each client machine:**
   See [CLAUDE_CONFIG.md](CLAUDE_CONFIG.md) for detailed client setup instructions.

   Quick setup:
   ```bash
   # Copy bridge script to each machine
   mkdir -p ~/.local/bin
   cp mcp-bridge.py ~/.local/bin/
   chmod +x ~/.local/bin/mcp-bridge.py

   # Add MCP server using Claude CLI
   claude mcp add -e PYTHONUNBUFFERED=1 --scope user brave-search -- \
     python3 ~/.local/bin/mcp-bridge.py http://${UNRAID_IP}:8011/mcp
   ```

---

## Configuration

### Brave Search MCP

Requires API key from [Brave Search](https://brave.com/search/api/).

```yaml
environment:
  BRAVE_API_KEY: "your-api-key-here"
```

### Obsidian MCP

Requires connection to your sync server. Path mapping:
- Host path: `/path/to/obsidian/vault`
- Container path: `/vault`

---

## Management

### View Logs
```bash
docker logs mcp-brave-search
docker logs mcp-sequential-thinking
```

### Restart Services
```bash
docker-compose restart
```

### Update All
```bash
docker-compose pull
docker-compose up -d
```

---

## Troubleshooting

### Service Not Responding
1. Check container status: `docker ps -a | grep mcp`
2. Review logs: `docker logs <container-name>`
3. Verify ports: `netstat -tuln | grep 801`

### Obsidian Connection Issues
1. Verify sync server is running
2. Check vault path permissions
3. Test network access from container

---

## Security Notes

- All MCP services run on internal network only
- No ports exposed to internet
- API keys stored in Docker secrets (TODO)
- Regular updates via `docker-compose pull`

---

## Usage

Once configured, Claude Code on any of your 4 machines can use Brave Search through the centralized Unraid server.

## TODO

- [ ] Implement Docker secrets for API keys
- [ ] Add Sequential Thinking MCP server
- [ ] Add Fetch Content MCP server
- [ ] Add healthcheck endpoints
- [ ] Set up monitoring in Grafana/Prometheus

---

## License

MIT - Feel free to use and modify for your setup.

**Last Updated:** 2026-01-16
