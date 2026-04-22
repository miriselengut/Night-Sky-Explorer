import requests
from bs4 import BeautifulSoup

#list of towns to choose from
towns = {
    "Waterbury": 4845193,
    "London": 2643743,
    "New York": 5128581,
    "Lakewood": 5100280,
    "Jerusalem": 281184,
    "South Bend": 4926563, 
    "Providence": 5224151
}

#settning up URL
town = towns["Waterbury"]
month = 5
year = 2026
day = 1

if town in towns.values():
    url = f"https://in-the-sky.org/data/planets.php?country=1840&reg1=4831725&reg2=4839373&town={town}&day={day}&month={month}&year={year}"

planets = {}

#setting up scraping
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

try:
    response = requests.get(url, headers=headers)
except Exception as e:
    print("Request failed", e)
    response = None

if response:
    soup = BeautifulSoup(response.text, 'html.parser')
else:
    return None
    
all_planets = soup.find_all("div", class_="greybox")

#find correct HTML location
for planet in all_planets:

    name = None
    planet_info = ""

    #finding and storing information about each planet 
    info = planet.find("p", class_="condensed")
    if info:
        name = info.find("a").get_text(strip=True)
        planet_info = name + " " + info.get_text(strip=True).replace(name, "").strip()

    #adding planet to dict (if not yet there)
    if name:
        if name not in planets:
            planets[name] = {"Info": "", "Rise": "", "Set": ""}

        planets[name]["Info"] = planet_info
        
        #finding and storing rise and set times about each planet
        timing = planet.find("table", class_="risesetinfo")
        if timing:
            rows = timing.find_all("tr")

            for row in rows:
                col = row.find_all("td")

                if len(col) == 2:
                    label = col[0].get_text(strip=True)
                    time = col[1].get_text(strip=True)

                    planets[name][label] = time

