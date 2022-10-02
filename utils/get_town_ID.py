import json
import requests
import os
from utils.request_to_api import request_to_api

def get_town_ID(town_name):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"

    querystring = {"query": town_name, "locale": "en_US", "currency": "USD"}

    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }


    response = request_to_api(url=url, headers=headers, querystring=querystring)
    data_response = json.loads(response.text)

    town_ID = data_response["suggestions"][0]["entities"][0]["destinationId"]

    return str(town_ID)

