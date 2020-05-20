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

### NOTE: The GET calls for a specific item and store required you to be logged in.
### ..... All GET and DELETE calls need an authorisation header to be sent along with the request.
### ......The GET call for all items and stores returns limited information to users not logged in and only provides complete information on loggin in.
### ......The DELETE calls for store,item,user are only Available to admins (the rules for admin can be changed in the source code). Also a user who is also an admin can't be deleted. BY DEFAULT, user_id = 1 IS ADMIN.
### ......The PUT and POST  calls for items need a user to be logged in and requires a fresh token. So you need to get the token refreshed to use those endpoints if original token expired. (For Security Purposes)


## Base url : <https://stores-rest-api-flask01.herokuapp.com/>
## End Points:

## GET:
### [/items](https://stores-rest-api-flask01.herokuapp.com/items)  - returns a list of items in json format. {name,price,store_id}
### Authorisation Header Required: {Bearer {{jwt_token}} returned by '/login' endpoint}
### [/item/<item_name>]()  - returns a specific item identified by its name from the database in json format. 
### Authorisation Header Required: {Bearer {{jwt_token}} returned by '/login' endpoint}

##          
### [/stores](https://stores-rest-api-flask01.herokuapp.com/stores) - returns a list of stores holding the items in json format.{name,items}
### Authorisation Header Required: {Bearer {{jwt_token}} returned by '/login' endpoint}
### [/store/<store_name>]() - returns a specific store identified by its name from the database in json format.
### Authorisation Header Required: {Bearer {{jwt_token}} returned by '/login' endpoint}

### [/user/<user_id>]() - returns a specific user identified by his name from the database in json format.
### Authorisation Header Required: {Bearer {{jwt_token}} returned by '/login' endpoint}
##
## POST:
### [/item/<item_name>]()  - adds a specific item to the database if not exists. Additional data required as Header body (price,store_id)
### Authorisation Header Required: {Bearer {{jwt_token}} returned by '/login' endpoint} with a fresh token
### [/store/<store_name>]() - adds a specific store to the database if not exists. Creates an empty store
### Authorisation Header Required: {Bearer {{jwt_token}} returned by '/login' endpoint} with a fresh token
##
## PUT:
### [/item/<item_name>]()  - adds a specific item to the database if not exists, or updates it with new price.
### Authorisation Header Required: {Bearer {{jwt_token}} returned by '/login' endpoint} with a fresh token
##
## DELETE: ONLY ADMINS CAN DELETE DATA
### [/item/<item_name>]()  - deletes a specific item from the database. 
### Authorisation Header Required: {Bearer {{jwt_token}} returned by '/login' endpoint} 
### [/store/<store_name>]() - deletes a specific store from the database. 
### Authorisation Header Required: {Bearer {{jwt_token}} returned by '/login' endpoint} 
### [/user/user_id]() - deletes a specific store from the database. 
### Authorisation Header Required: {Bearer {{jwt_token}} returned by '/login' endpoint} 
##
## AUTH:
### [/register]() - registers a new user taking username and password as header body. 
### Additional data required as Header body: {username,password}
### [/login]() - logs in a user taking username and password as header body and issues a JWT token to be required with the GET calls for specific item and store as Authorisation header. 
### Additional data reuqired as Header body: {username,password}
### [/logout]() - logs out a user taking username and password as header body and deactivates the JWT issued earlier for specific item and store as Authorisation header. 
### Additional data reuqired as Header body: {username,password}

### [/refresh]() - refreshes the token of the logged in user by takin in his refresh token issued while login. 
### Authorisation Header Required: {Bearer {{refresh_token}} returned by '/login' endpoint} 

 
