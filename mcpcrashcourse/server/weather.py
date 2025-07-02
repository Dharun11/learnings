from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

#initializing the FastMCP server
mcp = FastMCP("weather")


## Weather API endpoint
NEWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


async def make_news_request(url:str)-> dict[str,Any] | None:
    """
    Makes a request to the weather API and returns the JSON response.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
        }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers,timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    return None
    

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
        Event: {props.get('event', 'Unknown')}
        Area: {props.get('areaDesc', 'Unknown')}
        Severity: {props.get('severity', 'Unknown')}
        Description: {props.get('description', 'No description available')}
        Instructions: {props.get('instruction', 'No specific instructions provided')}
        """
        
        
@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NEWS_API_BASE}/alerts/active/area/{state}"
    data = await make_news_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.resource("config://app", title="Application Configuration")
def get_config() -> str:
    """Static configuration data"""
    return "App configuration here"

@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"