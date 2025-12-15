from fastmcp import FastMCP 
import uvicorn
from datetime import datetime, timedelta

server = FastMCP("weather-tools")

@server.tool()
def get_weather_forecast(destination: str, date: str) -> str:
    """
    Get weather forecast for a destination on a specific date.
    Date format: YYYY-MM-DD
    """
    # Mock weather data - in production, connect to OpenWeatherMap or similar
    weather_data = {
        "Barcelona": {
            "summer": "Sunny, 28-32°C, perfect for beaches and outdoor activities",
            "winter": "Mild, 10-15°C, good for sightseeing with light jacket",
            "spring": "Pleasant, 18-24°C, ideal for walking tours",
            "fall": "Comfortable, 20-26°C, great for outdoor dining"
        },
        "Paris": {
            "summer": "Warm, 20-25°C, occasional showers, bring umbrella",
            "winter": "Cold, 2-8°C, dress warmly for outdoor attractions",
            "spring": "Mild, 10-18°C, perfect for cafe visits",
            "fall": "Cool, 8-15°C, beautiful fall foliage"
        },
        "Tokyo": {
            "summer": "Hot & humid, 25-30°C, consider indoor attractions",
            "winter": "Cool, 2-10°C, great for temple visits",
            "spring": "Mild, 15-20°C, cherry blossom season if timing is right",
            "fall": "Comfortable, 18-23°C, ideal for exploring"
        }
    }
    
    # Determine season based on date
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d")
        month = target_date.month
        
        if month in [12, 1, 2]:
            season = "winter"
        elif month in [3, 4, 5]:
            season = "spring"
        elif month in [6, 7, 8]:
            season = "summer"
        else:
            season = "fall"
    except:
        season = "summer"  # default
    
    # Get destination weather or default
    dest_weather = weather_data.get(destination, weather_data["Barcelona"])
    forecast = dest_weather.get(season, "Pleasant weather for travel")
    
    return f"Weather forecast for {destination} on {date}: {forecast}"

@server.tool()
def get_seasonal_advice(destination: str) -> str:
    """Get general seasonal travel advice for a destination."""
    advice = {
        "Barcelona": "Summer: Beach weather, bring sunscreen. Winter: Mild but rainy.",
        "Paris": "Spring is best for outdoor activities. Winter requires warm clothing.",
        "Tokyo": "Spring for cherry blossoms. Summer can be very humid.",
        "New York": "Fall has beautiful foliage. Winter is cold with potential snow."
    }
    
    return advice.get(destination, "Generally pleasant year-round. Check specific dates for details.")

if __name__ == "__main__":
    server.run(transport="sse", port=3335)
