import pandas as pd
from apyori import apriori

dataset = pd.read_csv('store_transactions.csv', header=None)
row, col = dataset.shape

transactions = []
for i in range(0, row):
    transactions.append([str(dataset.values[i,j]) for j in range(0, col)])

association_rules = apriori(transactions, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2)
association_results = list(association_rules)

req_rules = association_results[:3]

for item in req_rules:
    pair = item[0]
    items = [x for x in pair]
    print(items[0] + " , " + items[1])

