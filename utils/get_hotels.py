import os
import json
from utils.request_to_api import request_to_api


def get_hotels(town_ID, checkIn, checkOut):
    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {
        "destinationId": town_ID,
        "pageNumber": "1",
        "pageSize": "25",
        "checkIn": checkIn,
        "checkOut": checkOut,
        "adults1": "1",
        "sortOrder": "PRICE",
        "locale": "ru_RU",
        "currency": "RUB",
    }

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    }

    response = request_to_api(url=url, headers=headers, querystring=querystring)

    data_response = json.loads(response.text)

    result_hotels = data_response["data"]["body"]["searchResults"]["results"]

    return result_hotels
