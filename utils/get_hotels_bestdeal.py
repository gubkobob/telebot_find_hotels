import os
import json
import requests
import datetime
from utils.request_to_api import request_to_api
import re


def get_hotels_bestdeal(town_ID, min_price, max_price):

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    checkIn = str(today)
    checkOut = str(tomorrow)

    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": town_ID, "pageNumber": "1", "pageSize": "25", "checkIn": checkIn,
                   "checkOut": checkOut, "adults1": "1", "priceMin": min_price, "priceMax": max_price, "sortOrder": "PRICE",
                   "locale": "ru_RU", "currency": "RUB"}

    headers = {
        "X-RapidAPI-Key": "dd5efb31b8msh0e3c63ba7041327p1ff064jsna74cd4544dad",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }


    response = request_to_api(url=url, headers=headers, querystring=querystring)

    data_response = json.loads(response.text)

    result_hotels = data_response["data"]["body"]["searchResults"]["results"]

    return result_hotels
