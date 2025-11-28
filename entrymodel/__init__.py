#Taka Irizarry
#iriz@pdx.edu

from .model_sqlite3 import UserModel

_model = UserModel()

# Function to get the singleton instance of UserModel
# usage 
# from entrymodel import get_model
# users = get_model()
def get_model() -> UserModel:
    return _model