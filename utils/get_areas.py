import json
import requests
import re
import os

def get_areas(town_name="new york"):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"

    querystring = {"query": town_name, "locale": "en_US", "currency": "USD"}

    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    pattern1 = r'(?<="CITY_GROUP",).+?[\]]'
    find = re.search(pattern1, response.text)
    if find:
        data_response = json.loads(f"{{{find[0]}}}")

    pattern = r"<.*>,"
    cities = []
    for area in data_response["entities"]:
        name = re.sub(pattern, "", area["caption"])
        cities.append({'city_name': name, "destination_id": area["destinationId"]})

    return cities

