import requests
import json
import csv

planets = [
    "Mercury",
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "The Moon"
]

def get_picture(planet_name):
    if planet_name not in planets:
        return None

    url = f"https://images-api.nasa.gov/search?q={planet_name}"
    print("URL used::", url)

    keywords = ["global", "atmosphere", "colored", "filtered", "global view", "hemisphere", "full-disk", 
                "planetary disk", "natural color", "false color", "infrared", "composite", "mosaic", 
                "atmosphere", "clouds", "cloud cover", "storm", "aerosol"]

    bad_words = ["celebration", "animation" "artist concept", "illustration", "render", "animation", "simulation", "diagram", "enhanced"]
    response = requests.get(url)
    data = response.json()

    items = data["collection"]["items"]

    href = items[0]["href"]


    for item in items:
        #image = items[0]["links"][0]["href"]
        if "data" not in item or "links" not in item:
            continue
            
        description = item["data"][0].get("description", "").lower()

        if any(word in description for word in bad_words):
            continue

        if any(word in description for word in keywords):
            return f"Link to image: " + item["links"][0]["href"]

    return None

if __name__ == "__main__":
    print(get_picture("Venus"))