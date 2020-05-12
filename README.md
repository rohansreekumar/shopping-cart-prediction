# shopping-cart-prediction
predict the shopping cart of a user using associative rule mining (Apriori algorithm)

- import the libraries - pandas, apyori, pymongo
- run mongodb on port 27017
- add the csv file to mongodb using the command : mongoimport --type csv -d test -c orders --headerline --drop store_transactions.csv 
- the csv file has 22000 dummy orders from users with id between 1-50
- run the python file

Input :
- user id of the person

Output :
- the output will be the top most frequently bought together items by the user (provided the user has more than 50 orders and bought the frequent items atleast 10 times)
- if no frequent set can be found from the users purchase history, the total orders list is used to predict items
