from fastmcp import FastMCP 
import uvicorn

server = FastMCP("destination-search-tools")

@server.tool()
def search_destination(destination: str) -> str:
    """Search for tourist attractions, landmarks, and activities in a destination."""
    # In production, you'd connect to a real API like Google Places or Yelp
    attractions = {
        "Barcelona": [
            "Sagrada Familia",
            "Park Güell", 
            "La Rambla",
            "Gothic Quarter",
            "Camp Nou Stadium",
            "Barcelona Beach",
            "Magic Fountain Show"
        ],
        "Paris": [
            "Eiffel Tower",
            "Louvre Museum",
            "Notre-Dame Cathedral",
            "Montmartre",
            "Seine River Cruise",
            "Champs-Élysées"
        ],
        "Tokyo": [
            "Shibuya Crossing",
            "Tokyo Skytree",
            "Senso-ji Temple",
            "Tsukiji Outer Market",
            "Shinjuku Gyoen National Garden",
            "Akihabara Electric Town"
        ],
        "New York": [
            "Statue of Liberty",
            "Central Park",
            "Times Square",
            "Empire State Building",
            "Broadway Show",
            "Metropolitan Museum of Art"
        ]
    }
    
    default_attractions = [
        "Local museums",
        "Historic landmarks",
        "Popular restaurants",
        "Shopping districts",
        "Parks and gardens",
        "Cultural centers"
    ]
    
    result = attractions.get(destination, default_attractions)
    return f"Top attractions in {destination}: " + ", ".join(result)

if __name__ == "__main__":
    server.run(transport="sse", port=3334)
