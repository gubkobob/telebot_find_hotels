import os
import json
import requests
import datetime


def get_hotels(town_ID):

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    checkIn = str(today)
    checkOut = str(tomorrow)

    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId":town_ID,"pageNumber":"1","pageSize":"25","checkIn":checkIn,"checkOut":checkOut,"adults1":"1","sortOrder":"PRICE","locale":"en_US","currency":"USD"}

    headers = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data_response = json.loads(response.text)

    result_hotels = data_response["data"]["body"]["searchResults"]["results"]

    return result_hotels
