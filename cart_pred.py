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

    association_rules = apriori(transactions, min_support=min_support, min_confidence=0.2, min_lift=3, min_length=2)
    association_results = list(association_rules)

    req_rules = association_results[:3]
    return req_rules


if __name__ == '__main__':
    dataset = read_mongo('test', 'orders', {})

    #taking user id as input
    print("Enter the user ID (1-100):")
    id = input()
    id = int(id)

    if id > 50:
        print("User ID not found, returning the most frequent items bought by customers")

    # extracting orders by the user from the whole orders dataset
    user_orders = dataset.loc[dataset['User ID'] == id]
    user_orders = user_orders.drop('User ID', 1)
    row, col = user_orders.shape

    #dropping the 1st column which is the user id
    dataset = dataset.drop('User ID', 1)

    #if no of ordersby user is more than 50, use the user_orders, else use the whole dataset
    if row > 50:
        mining_dataset = user_orders
        user_orders_row, user_orders_col = user_orders.shape
        support = 10/user_orders_row
        min_support = support

    else:
        mining_dataset = dataset
        min_support = 0.0045

    req_rules = apriori_algo(mining_dataset, min_support)

    if len(req_rules) == 0:
        req_rules = apriori_algo(dataset, 0.0045)

    for item in req_rules:
        pair = item[0]
        items = [x for x in pair]
        print(items[0] + " , " + items[1])

