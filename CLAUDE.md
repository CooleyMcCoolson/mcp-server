# MCP Server - Claude Context

## Project Overview
Centralized Model Context Protocol (MCP) servers running on Unraid. Provides shared AI context services to 4 machines on the network.

## Architecture
- **Host:** Unraid server (${UNRAID_HOSTNAME})
- **IP:** ${UNRAID_IP}
- **Storage:** `/mnt/cache_nvme/appdata/mcp`
- **Network:** Internal bridge network (172.20.0.0/16)
- **Services:** Brave Search, Sequential Thinking, Fetch Content, Obsidian (TODO)

## Services

| Service | Container | Port | Purpose |
|---------|-----------|------|---------|
| Brave Search | mcp-brave-search | 8011 | Web search via Brave API |
| Sequential Thinking | mcp-sequential-thinking | 8012 | Complex reasoning chains |
| Fetch Content | mcp-fetch-content | 8013 | Web content retrieval |
| Obsidian | mcp-obsidian | 8014 | Vault access (TODO) |

## Configuration Files
- `docker-compose.yml` - Service definitions
- `.env` - Environment variables (API keys, ports)
- `setup.sh` - Deployment script
- `README.md` - Full documentation

## Common Commands

```bash
# SSH to Unraid
ssh root@${UNRAID_IP}

# Navigate to project
cd /mnt/cache_nvme/appdata/mcp

# View running containers
docker ps | grep mcp

# View logs
docker logs -f [service-name]

# Restart service
docker restart mcp-[service-name]

# Stop service
docker stop mcp-[service-name]
```

## Troubleshooting

### Container not starting
```bash
docker logs mcp-[service-name]
docker inspect mcp-[service-name]
```

### Port conflicts
Check ports in `.env` and `docker-compose.yml`

### Permission issues
```bash
chown -R nobody:users /mnt/cache_nvme/appdata/mcp
```

## TODO
- [ ] Complete Obsidian MCP setup with sync server integration
- [ ] Implement Docker secrets for API keys
- [ ] Add Prometheus metrics
- [ ] Configure backup/restore

## Related
- Unraid: ${UNRAID_IP} (${UNRAID_HOSTNAME})
- Laptop: ${LAPTOP_HOSTNAME} (${LAPTOP_TAILSCALE_IP} via Tailscale)
- Obsidian sync: Running on Unraid
- Project: ~/code/public/mcp-server
