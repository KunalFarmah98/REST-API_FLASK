from Models.user import UserModel

def authenticate(name,password):
    user = UserModel.find_by_username(name)
    if user and user.password == password:
        return user

def identity(payload):
    user_id= payload['identity']
    return UserModel.find_by_id(user_id)

