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


if __name__ == '__main__':
    dataset = read_mongo('test', 'orders', {})


    print("Enter the user ID (1-100):")
    id = input()

    print("id is :", id)
    id = int(id)

    user_orders = dataset.loc[dataset['User ID'] == id]
    user_orders = user_orders.drop('User ID', 1)
    row, col = user_orders.shape
    #print(user_orders)


    dataset = dataset.drop('User ID', 1)


    #print(dataset)

    if row > 50:
        mining_dataset = user_orders
        #print("inside if", row, col)

    else:
        mining_dataset = dataset

    transactions = []
    row, col = dataset.shape
    for i in range(0, row):
        #print("here")
        transactions.append([str(dataset.values[i,j]) for j in range(0, col)])
    print(transactions)

    association_rules = apriori(transactions, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2)
    association_results = list(association_rules)
    #print("here1")
    req_rules = association_results[:3]

    for item in req_rules:
        pair = item[0]
        items = [x for x in pair]
        print(items[0] + " , " + items[1])

