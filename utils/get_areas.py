import json
import re
import os
from utils.request_to_api import request_to_api

def get_areas(town_name="new york"):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"

    querystring = {"query": town_name, "locale": "ru_RU", "currency": "RUB"}

    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = request_to_api(url=url, headers=headers, querystring=querystring)

    pattern1 = r'(?<="CITY_GROUP",).+?[\]]'
    find = re.search(pattern1, response.text)
    if find:
        data_response = json.loads(f"{{{find[0]}}}")

    pattern2 = r"<span class='highlighted'>"
    pattern3 = r"<\/span>"

    cities = []
    for area in data_response["entities"]:
        name = re.sub(pattern2, "", area["caption"])
        name = re.sub(pattern3, "", name)
        cities.append({'city_name': name, "destination_id": area["destinationId"]})

    return cities

