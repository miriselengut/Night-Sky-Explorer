import requests
from bs4 import BeautifulSoup

town = {
    "Waterbury": 4845193,
    "London": 2643743,
    "New York": 5128581,
    "Lakewood": 5100280,
    "Jerusalem": 281184,
    "South Bend": 4926563
}

town = town["Waterbury"]

month = 5
year = 2026
day = 1

url = f"https://in-the-sky.org/data/planets.php?country=1840&reg1=4831725&reg2=4839373&town={town}&day={day}&month={month}&year={year}"

planets = {}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

all_planets = soup.find_all("div", class_="greybox")

for planet in all_planets:

    info = planet.find("p", class_="condensed")

    name = None
    planet_info = ""

    if info:
        name = info.find("a").get_text(strip=True)
        planet_info = name + " " + info.get_text(strip=True).replace(name, "").strip()
        print(planet_info)

    timing = planet.find("table", class_="risesetinfo")

    if name:
        if name not in planets:
            planets[name] = {"Info": "", "Rise": "", "Set": ""}

        planets[name]["Info"] = planet_info

        if timing:
            rows = timing.find_all("tr")

            for row in rows:
                col = row.find_all("td")

                if len(col) == 2:
                    label = col[0].get_text(strip=True)
                    time = col[1].get_text(strip=True)

                    planets[name][label] = time

print(planets["The Moon"])

