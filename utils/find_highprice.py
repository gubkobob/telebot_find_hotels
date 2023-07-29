
from operator import itemgetter

def highprice(hotels, count, max_count):

    if count > max_count:
        count = max_count

    my_result_hotels = []
    try:

        for hotel in hotels:
            my_hotel = dict()
            my_hotel["name"] = hotel["name"]
            my_hotel["address"] = hotel["address"]["streetAddress"]
            my_hotel["distance"] = hotel["landmarks"][0]["distance"]
            my_hotel["price"] = hotel["ratePlan"]["price"]["exactCurrent"]
            my_hotel["id"] = hotel["id"]
            my_result_hotels.append(my_hotel)

        my_result_hotels = sorted(my_result_hotels, key=itemgetter("price"), reverse=True)

        if len(my_result_hotels) < count:
            count = len(my_result_hotels)
    except Exception:
        print("в базе нет какого-то параметра ")

    return my_result_hotels[:count]
