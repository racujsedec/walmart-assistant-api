# Optional standalone MCP server. Install requirements-optional.txt.
# SECURITY: This demo wrapper is not authenticated; do not expose to a network.
from mcp.server.fastmcp import FastMCP
from app.rag.retrieve import search_policy
mcp=FastMCP('demo-policy-tools')
@mcp.tool()
def search_demo_policy(query:str)->list[dict]:return search_policy(query)
if __name__=='__main__':mcp.run()
