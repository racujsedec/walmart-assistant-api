"""Illustrative MCP wrapper around the existing authorized Python tool.
Requires optional `mcp` package and backend imports on PYTHONPATH.
This is an alternative transport to the direct in-process LangGraph tool.
"""
from mcp.server.fastmcp import FastMCP
from app.order_tool import get_order_status

mcp = FastMCP("associate-order-tools")

@mcp.tool()
async def order_status(order_id: str) -> dict:
    # DEMO ONLY: fixed permission. Real MCP servers validate caller identity and RBAC.
    return await get_order_status(order_id, ["orders:read"])

if __name__ == "__main__":
    mcp.run()
