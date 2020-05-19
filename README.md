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
