import requests
import json
import csv

# list of planets
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
    # if bad input
    if planet_name not in planets:
        return None


    url = f"https://images-api.nasa.gov/search?q={planet_name}"

    #key words to filter responses
    keywords = ["global", "atmosphere", "colored", "filtered", "global view", "hemisphere", "full-disk", 
                "planetary disk", "natural color", "false color", "infrared", "composite", "mosaic", 
                "atmosphere", "clouds", "cloud cover", "storm", "aerosol"]

    bad_words = ["celebration", "animation", "artist concept", "illustration", "render", "animation", 
                "simulation", "diagram", "enhanced"]
    
    try:
        #get response from json
        response = requests.get(url)
        data = response.json()
        #access the data
        items = data["collection"]["items"]
    except Exception as e:
        print("Can't properly access image")
        return None

    #if missing something, skip image
    for item in items:
        if "data" not in item or "links" not in item:
            continue
        
        #get description, and make sure it includes keywords, and doesn't contain bad words
        description = item["data"][0].get("description", "").lower()

        if any(word in description for word in bad_words):
            continue

        if any(word in description for word in keywords):
            return f"Link to image: " + item["links"][0]["href"]

    return "Image Not Found"

if __name__ == "__main__":
    print(get_picture("Venus"))