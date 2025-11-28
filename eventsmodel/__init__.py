#Taka Irizarry
#iriz@pdx.edu

from .model_sqlite3 import EventModel
_model = EventModel()

#Return the singleton instance of EventModel
def get_model() -> EventModel:
    return _model