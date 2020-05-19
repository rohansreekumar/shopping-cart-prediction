import pandas as pd
from apyori import apriori
from pymongo import MongoClient

def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]

def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)
    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)
    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))
    # Delete the _id
    if no_id and '_id' in df:
        del df['_id']
    return df

def apriori_algo(mining_dataset, min_support):
    """ Read the dataframe and returns the frequent item set"""

    transactions = []
    row, col = mining_dataset.shape
    # converting the dataset into a list of lists for use in apriori method
    for i in range(0, row):
        transactions.append([str(mining_dataset.values[i, j]) for j in range(0, col)])
    # removing the null items in the transactions
    for i in range(0, row):
        transactions[i] = list(filter(None, transactions[i]))
    #applying apriori algorithm to the transactions
    association_rules = apriori(transactions, min_support=min_support, min_confidence=0.2, min_lift=3, min_length=2)
    association_results = list(association_rules)
    return association_results


if __name__ == '__main__':

    order_dataset = read_mongo('test', 'orders', {})
    store_dataset = read_mongo('test', 'stores', {})
    item_dataset = read_mongo('test', 'items', {})
    id = 1000
    # taking user id as input
    while id > 50:
        print("Enter the user ID (1-50):")
        id = input()
        id = int(id)
        if id > 50:
            print("User ID not found")

    #taking user input for preference of shopping type
    print("Do you want to create a unified shopping list (enter 1) or select a particular store to order (enter 2): ")
    selection = input()
    selection = int(selection)
    # if user selects unified shopping list
    if selection == 1:
        print("Enter the unified shopping list:")
        unified_shopping_list = input()
        #manipulating the user input(shopping list) to get a list of items
        shopping_list = unified_shopping_list.split(',')
        final_shopping_list = []
        for item in shopping_list:
            item = item.strip()
            final_shopping_list.append(item)

        #identifying the store type to which each of the item associates to
        store_types = []
        for item in final_shopping_list:
            if item in item_dataset['Item'].values:
                store_type = item_dataset.loc[item_dataset['Item'] == item]
                s_type = store_type['StoreType'].values
                item_storetype = item+"-"+s_type[0]
                store_types.append([item_storetype])
        print("The various types of stores needed are: ", store_types)

        #prediction part - where most frequent items are predicted
        print("The most frequently bought items are: ")
        # extracting orders by the user from the whole orders dataset
        user_orders = order_dataset.loc[order_dataset['User ID'] == id]
        user_orders = user_orders.drop('User ID', 1)
        row, col = user_orders.shape
        #dropping the 1st column which is the user id
        order_dataset = order_dataset.drop('User ID', 1)
        #if no of order sby user is more than 50, use the user_orders, else use the whole dataset
        if row > 50:
            mining_dataset = user_orders
            user_orders_row, user_orders_col = user_orders.shape
            support = 10/user_orders_row
            min_support = support
        else:
            mining_dataset = order_dataset
            min_support = 0.0045

        #calling the apriori_algo function
        req_rules = apriori_algo(mining_dataset, min_support)
        req_rules = req_rules[:3]

        if len(req_rules) == 0:
            req_rules = apriori_algo(order_dataset, 0.0045)

        for item in req_rules:
            pair = item[0]
            items = [x for x in pair]
            print(items[0] + " , " + items[1])

    # if user selects a particular store to order
    elif selection == 2:
        stores = store_dataset['StoreName'].tolist()
        stripped_store_df = store_dataset.drop('Storetype', 1)
        # prints the set of stores which are currently available
        print("The available stores are:", stores)
        print("Enter the store you would like to shop from:")
        input_store = input()
        if input_store not in stores:
            print("Not a valid store")
            exit()

        # extracting the list of items available in the selected store
        store_items = stripped_store_df.loc[stripped_store_df['StoreName'] == input_store]
        store_items = store_items.drop('StoreName', 1)
        store_items = store_items[:].values.tolist()
        store_items = list(filter(None, store_items[0]))
        print("The items available in the store are:")
        print(store_items)
        # predicting the most frequently bought items from the chosen store, if not enough orders, then no prediction
        min_support = 0.0025
        order_dataset = order_dataset.drop('User ID', 1)
        req_rules = apriori_algo(order_dataset, min_support)

        if len(req_rules) > 500:
            req_rules = req_rules[:500]

        print("The most frequently bought items are: ")
        predict_list = []
        item_found = False
        for item in req_rules:
            pair = item[0]
            items = [x for x in pair]
            if items[0] in store_items and items[1] in store_items:
                item_found = True
                item_list = items[0] + " , " + items[1]
                if item_list not in predict_list:
                    predict_list.append(item_list)
                    print(items[0] + " , " + items[1])

        if item_found == False:
            print("Not enough orders to predict the frequent items")

