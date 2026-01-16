#!/usr/bin/env python3
"""
MCP Bridge - Connects Claude Code (stdio) to Remote HTTP MCP Server
Author: Cooley McCoolson
Created: 2026-01-16

This script allows you to run MCP servers centrally on Unraid while
connecting to them from multiple machines via stdio.

Usage:
    mcp-bridge.py http://${UNRAID_IP}:8011/mcp
"""

import sys
import json
import urllib.request
import urllib.error
from typing import Any, Dict

class MCPBridge:
    """Bridges stdio MCP client to HTTP MCP server"""

    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.request_id = 1

    def send_response(self, response: Dict[str, Any]):
        """Send response to stdout"""
        json.dump(response, sys.stdout)
        sys.stdout.write("\n")
        sys.stdout.flush()

    def send_error(self, code: int, message: str):
        """Send error response"""
        self.send_response({
            "jsonrpc": "2.0",
            "id": self.request_id - 1,
            "error": {
                "code": code,
                "message": message
            }
        })

    def handle_request(self, request: Dict[str, Any]):
        """Handle incoming MCP request"""
        if "id" in request:
            self.request_id = request["id"]

        # Prepare HTTP request
        payload = json.dumps(request).encode("utf-8")

        try:
            req = urllib.request.Request(
                self.endpoint,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream"
                },
                method="POST"
            )

            # Send to remote MCP server
            with urllib.request.urlopen(req, timeout=30) as response:
                content_type = response.headers.get("Content-Type", "")

                if "text/event-stream" in content_type:
                    # Handle SSE response
                    result = self._parse_sse_response(response)
                else:
                    # Handle plain JSON response
                    result = json.loads(response.read().decode("utf-8"))

            # Forward response back to client
            self.send_response(result)

        except urllib.error.HTTPError as e:
            self.send_error(e.code, f"HTTP Error: {e.reason}")
        except urllib.error.URLError as e:
            self.send_error(-32603, f"Connection Error: {e.reason}")
        except Exception as e:
            self.send_error(-32603, f"Internal Error: {str(e)}")

    def _parse_sse_response(self, response):
        """Parse Server-Sent Events (SSE) response"""
        for line in response:
            line = line.decode("utf-8").strip()
            if line.startswith("data: "):
                data = line[6:]  # Remove "data: " prefix
                return json.loads(data)
        raise ValueError("No data in SSE response")

    def run(self):
        """Main loop - read from stdin, forward to HTTP, write to stdout"""
        sys.stderr.write(f"MCP Bridge: Connecting to {self.endpoint}\n")
        sys.stderr.flush()

        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue

                try:
                    request = json.loads(line)
                    self.handle_request(request)
                except json.JSONDecodeError as e:
                    self.send_error(-32700, f"Parse Error: {str(e)}")

        except KeyboardInterrupt:
            sys.stderr.write("\nMCP Bridge: Shutting down\n")
            sys.stderr.flush()


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: mcp-bridge.py <mcp_endpoint_url>\n")
        sys.stderr.write("Example: mcp-bridge.py http://${UNRAID_IP}:8011/mcp\n")
        sys.exit(1)

    endpoint = sys.argv[1]

    # Validate URL format
    if not endpoint.startswith(("http://", "https://")):
        sys.stderr.write("Error: Endpoint must start with http:// or https://\n")
        sys.exit(1)

    bridge = MCPBridge(endpoint)
    bridge.run()


if __name__ == "__main__":
    main()
