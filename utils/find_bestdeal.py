from operator import itemgetter
import re


def bestdeal(hotels, count, min_dist, max_dist, max_count=10):
    if count > max_count:
        count = max_count

    my_result_hotels = []
    try:
        for hotel in hotels:
            distance = hotel["landmarks"][0]["distance"]
            distance = re.sub(r"\,", ".", distance)
            distance = float(re.sub(r"км", "", distance))
            if distance <= 1:
                k = 1
            elif 1 < distance <= 3:
                k = 1.5
            elif 3 < distance <= 5:
                k = 2
            else:
                k = 3

            if min_dist <= distance <= max_dist:
                my_hotel = dict()
                # my_hotel["dist_digits"] = distance
                my_hotel["name"] = hotel["name"]
                my_hotel["address"] = hotel["address"]["streetAddress"]
                my_hotel["distance"] = hotel["landmarks"][0]["distance"]
                my_hotel["price"] = hotel["ratePlan"]["price"]["exactCurrent"]
                my_hotel["id"] = hotel["id"]
                my_hotel["koef"] = (
                    k * my_hotel["price"]
                )  # коэффициент для выбора наилучшего отеля по расстоянию и цене
                my_result_hotels.append(my_hotel)

        my_result_hotels = sorted(my_result_hotels, key=itemgetter("koef"))

        if len(my_result_hotels) < count:
            count = len(my_result_hotels)

    except Exception:
        print("в базе нет какого-то параметра ")

    return my_result_hotels[:count]
