from fastmcp import FastMCP 
import uvicorn

server = FastMCP("currency-tools")

@server.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert amount from one currency to another using current exchange rates."""
    # Mock exchange rates - in production, use a real API like ExchangeRate-API
    exchange_rates = {
        "USD": {"EUR": 0.92, "GBP": 0.79, "JPY": 148.0, "USD": 1.0},
        "EUR": {"USD": 1.09, "GBP": 0.86, "JPY": 161.0, "EUR": 1.0},
        "GBP": {"USD": 1.27, "EUR": 1.16, "JPY": 187.0, "GBP": 1.0},
        "JPY": {"USD": 0.0068, "EUR": 0.0062, "GBP": 0.0053, "JPY": 1.0}
    }
    
    # Default to USD if currency not found
    rates = exchange_rates.get(from_currency.upper(), exchange_rates["USD"])
    rate = rates.get(to_currency.upper(), 1.0)
    
    converted_amount = round(amount * rate, 2)
    return converted_amount

@server.tool()
def get_currency_info(destination: str) -> str:
    """Get currency information for a specific destination."""
    currency_info = {
        "Barcelona": "Currency: Euro (EUR)",
        "Paris": "Currency: Euro (EUR)",
        "London": "Currency: British Pound (GBP)",
        "Tokyo": "Currency: Japanese Yen (JPY)",
        "New York": "Currency: US Dollar (USD)",
        "Sydney": "Currency: Australian Dollar (AUD)",
        "Dubai": "Currency: UAE Dirham (AED)"
    }
    
    return currency_info.get(destination, "Currency: Check local currency for this destination")

if __name__ == "__main__":
    server.run(transport="sse", port=3336)
