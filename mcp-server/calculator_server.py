from fastmcp import FastMCP 
import uvicorn

server = FastMCP("calculator-tools")

@server.tool()
def calculate(expression: str) -> float:
    """Evaluate a mathematical expression."""
    # Simple calculator - in production, use a safer evaluation method
    try:
        # Remove any unsafe characters
        safe_chars = "0123456789+-*/(). "
        cleaned_expr = ''.join(c for c in expression if c in safe_chars)
        
        # Evaluate safely using eval (for educational purposes only)
        # In production, use a safer alternative like ast.literal_eval for limited expressions
        result = eval(cleaned_expr)
        return float(result)
    except Exception as e:
        return f"Error calculating expression: {str(e)}"

@server.tool()
def calculate_daily_budget(total_budget: float, days: int) -> float:
    """Calculate daily budget from total budget and number of days."""
    if days <= 0:
        return 0.0
    return round(total_budget / days, 2)

@server.tool()
def calculate_with_tax(amount: float, tax_percentage: float) -> float:
    """Calculate total amount including tax."""
    tax_amount = amount * (tax_percentage / 100)
    return round(amount + tax_amount, 2)

@server.tool()
def split_cost(total_cost: float, people: int) -> float:
    """Split total cost equally among people."""
    if people <= 0:
        return total_cost
    return round(total_cost / people, 2)

if __name__ == "__main__":
    server.run(transport="sse", port=3337)
