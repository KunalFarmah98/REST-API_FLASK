from db import db

# extending db.Model to make it use alchemy
class StoreModel(db.Model):

    __tablename__ = "Stores"
    id  = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))

    # making items realted to store
    # this gives a list of items in that store
    items = db.relationship('ItemModel',lazy='dynamic')
    
    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls,name):
        # SELECT * FROM Items WHERE name = name LIMIT = 1
        return cls.query.filter_by(name=name).first()


    def save_to_db(self):

        # adding the current object (self) to the database
        db.session.add(self)
        db.session.commit()
    

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

        