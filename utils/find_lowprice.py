
from operator import itemgetter
# from utils.get_hotels import get_hotels
# from utils.get_town_ID import get_town_ID

def lowprice(hotels, count, max_count):

    if count > max_count:
        count = max_count

    my_result_hotels = []

    for hotel in hotels:
        my_hotel = dict()
        my_hotel["name"] = hotel["name"]
        my_hotel["address"] = hotel["address"]["streetAddress"]
        my_hotel["distance"] = hotel["landmarks"][0]["distance"]
        my_hotel["price"] = hotel["ratePlan"]["price"]["exactCurrent"]
        my_hotel["photos"] = "some photos"
        my_result_hotels.append(my_hotel)

    my_result_hotels = sorted(my_result_hotels, key=itemgetter("price"))

    if len(my_result_hotels) < count:
        count = len(my_result_hotels)

    return my_result_hotels[:count]
    # for i in range(count):
    #     print(i + 1, "\n", my_result_hotels[i])



# if __name__ == "__main__":
#     print(lowprice(get_hotels(get_town_ID("new york")), count=4, max_count=100))