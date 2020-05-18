from db import db

# extending db.Model to make it use alchemy
class ItemModel(db.Model):

    __tablename__ = "Items"
    id  = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # link to stores database
    # primary key of stores table foreign key to access store from items
    store_id = db.Column(db.Integer,db.ForeignKey('Stores.id'))
    # WE CAN'T DELETE THE STORE WHO'S ID IS USED AS A FOREIGN KEY IN ITEMS

    # SQLAlchemy Joins both the items and stores table to make life easier
    store = db.relationship('StoreModel')
    
    def __init__(self, name, price,  store_id ):
        self.name = name
        self.price = price
        self.store_id = store_id

    # we are not looking into the table unless we call json
    # (slightly slower)
    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls,name):
        # SELECT * FROM Items WHERE name = name LIMIT = 1
        return cls.query.filter_by(name=name).first()


    def save_to_db(self):

        # adding the current object (self) to the database
        db.session.add(self)
        db.session.commit()
    

    def delte_from_db(self):
        db.session.delete(self)
        db.session.commit()

        