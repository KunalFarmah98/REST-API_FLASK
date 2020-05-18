# REST-API_FLASK
# A simple REST API made using Flask hosted on Heroku.
### Capable of adding, updating, removing data in the PostgraceSQL database while being completely secure.
### Ability for secure sign up and login facility via simple endpoints.

#

## Made using Flask and Python-3.7.4
## Uses FLASK-RESTful for seamless integration into REST principle.
## Uses FLASK-JWT with 30 min token validity for security and authentication, just login again and get issued a new token (To be Updated with auto refreshing soon)
## Uses SQLAlchemy for integration with sqlite for testing on local machine and postgrace for use online
## Clean and reusable code for extending the features further.

#

## Base url : <https://stores-rest-api-flask01.herokuapp.com/>
## End Points:

## GET:
### [/items](https://stores-rest-api-flask01.herokuapp.com/items)  - returns a list of items in json format. {name,price,store_id}
### [/item/<item_name>]()  - returns a specific item identified by its name from the database in json format. 
### Header Body: {name,price,store_id}, 
### Authorisation Header Required: {JWT {{jwt_token}} returned by '/auth' endpoint}
##          
### [/stores](https://stores-rest-api-flask01.herokuapp.com/stores) - returns a list of stores holding the items in json format.{name,items}
### [/store/<store_name>]() - returns a specific store identified by its name from the database in json format.
### Header body : {name,items},
### Authorisation Header Required: {JWT {{jwt_token}} as returned by '/auth' endpoint}
##
## POST:
### [/item/<item_name>]()  - adds a specific item to the database if not exists. Additional data reuqired as Header body (price,store_id)
### [/store/<store_name>]() - adds a specific store to the database if not exists. Creates an empty store
##
## PUT:
### [/item/<item_name>]()  - adds a specific item to the database if not exists, or updates it with new price.
##
## DELETE:
### [/item/<item_name>]()  - deletes a specific item from the database. 
### [/store/<store_name>]() - deletes a specific store from the database. 
##
## AUTH:
### [/register]() - registers a new user taking username and password as header body. 
### Additional data required as Header body: {username,password}
### [/auth]() - logs in a user taking username and password as header body and issues a JWT token to be required with the GET calls for specific item and store as Authorisation header. 
### Additional data reuqired as Header body: {username,password}

 
