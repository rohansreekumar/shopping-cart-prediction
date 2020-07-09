from pymongo import MongoClient
from datetime import datetime


if __name__ == '__main__':

    conn = MongoClient('localhost', 27017)
    db = conn.test
    retail_data = db.retail
    retail_list = retail_data.find()
    order_data = db.shop_orders
    order_list = order_data.find()


    # Taking input for item name and store name for price prediction
    print("Enter the commodity for which the price needs to be predicted : (Banana/ Granny Smith Apples/ Strawberry/ Mango/ Blueberry/ Kiwi / Mulberry / Peach/ Banana Robesta/ Apple Modi/ Mango Alphons) :")
    selection = input()
    item_name = selection
    print("Enter store name: (testStore / testStore2) :")
    selection = input()
    store_name = selection


    present = datetime.now()
    predicted_price = None

    # case 1 - checking the list of orders (in past 24hrs) to find price of the given item
    for order in order_list:
        if order['store'] == store_name:
            datetime_object = datetime.strptime(order['createdAt'], '%Y-%m-%d %H:%M:%S.%f')
            timediff = present - datetime_object

            if timediff.days < 1:
                for item in order['items']:
                    if item['name'] == item_name:
                        predicted_price = item['rate']
                        print("Predicted price:" ,predicted_price , "per 500 gms based on last 24hr orders")

    # case 2 - checking the list of orders (more than 24hrs ago) to find price of the given item
    curr_store_loc = None
    if predicted_price == None:
        order_list = order_data.find()
        for order in order_list:
            if order['store'] == store_name:
                curr_store_loc = order['address']['locality']
                for item in order['items']:
                    if item['name'] == item_name:
                        predicted_price = item['rate']
                        print("Predicted price:", predicted_price, "per 500 gms based on orders from last few days")
                        break
                if predicted_price != None:
                    break

                # case 3 - checking the list of orders to find stores nearby to find price of the given item
                else:
                    other_order_list = order_data.find()
                    for order in other_order_list:
                        if order['store'] != store_name and order['address']['locality'] == curr_store_loc:
                            for item in order['items']:
                                if item['name'] == item_name:
                                    predicted_price = item['rate']
                                    print("Predicted price:", predicted_price, "per 500 gms based on other stores in the location")
                                    break
                            if predicted_price != None:
                                break

    # case 4 - no prediction possible
    if predicted_price == None:
        print("No prediction can be made")