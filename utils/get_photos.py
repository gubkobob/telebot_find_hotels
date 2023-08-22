from utils.request_to_api import request_to_api
import os
import json
import re


def get_photos(hotel_id, n_photos, max_n_photos=10):
    if n_photos > max_n_photos:
        n_photos = max_n_photos

    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": str(hotel_id)}

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    }

    response = request_to_api(url=url, headers=headers, querystring=querystring)
    data_response = json.loads(response.text)
    photos_list = []
    i = 0

    for photo in data_response["hotelImages"]:
        if i < n_photos:
            photo_with_size = re.sub(r"{size}", "w", photo["baseUrl"])
            photos_list.append(photo_with_size)
        else:
            break
        i += 1
    return photos_list


# print(get_photos("1178275040"))
