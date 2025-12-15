# Replace the old mcp.server.fastapi import
from fastmcp import FastMCP  # This is the correct import for v2.14.1

# Create server with FastMCP class instead of MCPServer
mcp = FastMCP("budget-tools")  # Changed from server = MCPServer("budget-tools")

@mcp.tool()  # Changed from @server.tool()
def estimate_budget(destination: str, days: int) -> float:
    """Estimate travel budget in USD."""
    base_cost = 100
    return base_cost * days

if __name__ == "__main__":
    # Changed from server.run(port=3333)
    mcp.run(transport="sse", port=3333)  # FastMCP handles ports differently - see note below
