# shopping-cart-prediction

predict the shopping cart of a user using associative rule mining (Apriori algorithm)

- import the libraries - pandas, apyori, pymongo
- run mongodb on port 27017
- add the csv files to mongodb using the command : mongoimport --type csv -d db_name -c collection_name --headerline --drop csv_file 
- there are 3 csv files:
    - store_transactions - contains the total list of orders from all customers
    - store_info - contains info about the store and the items it sells
    - items - contains info about the various items and their type
- run the python file

Input :
- user id of the person
- 1 or 2 based on whether user wants to provide a unified shopping list or choose a particular shop to order
- if 1 chosen in 2nd step
    - user needs to input the unified shopping list
- if 2 chosen in 2nd step
    - user needs to input store name from the given list of store names
    
    
Output :

- if user input is 1 (unified shopping list)
    - various types of stores needed to complete the customer order
    - the top most frequently bought together items

- if user input is 2 (choose a particular shop to order)
    - various items that are available in the selected store
    - the top most frequently bought together items from the store   
 
- if no frequent set can be found from the users purchase history, the total orders list is used to predict items


# price prediction

price_pred.py predicts the price of an item based on the following criteria:
1. If the retailer has sold the same item in the last 24hrs (it has to have same quantity and UOM) then return that price
2. If the retailer hasn't sold in the last 24hrs,check for his historical orders and use it to return the price
3. If the retailer hasn't sold it at all, check for the same item in the same location and return that price.
4.else,  no prediction

- There are 3 json files 
1. retail.json
2 order.json
3 list.json

Input:
- The item for which the price needs to be predicted ( Currently items must be one of the following - 
Banana/ Granny Smith Apples/ Strawberry/ Mango/ Blueberry/ Kiwi / Mulberry / Peach/ Banana Robesta/ Apple Modi/ Mango Alphons)

- The store name  ( Currently must be one of - testStore / testStore2)

Output :
- Predicted price of the item per UOM

