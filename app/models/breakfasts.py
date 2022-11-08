from app import db
from flask import abort,make_response

class Breakfast(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    rating = db.Column(db.Float)
    prep_time = db.Column(db.Integer)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.menu_id'), default=None)
    menu = db.relationship('Menu', back_populates='breakfasts')

    def dictionfy(self):
        return_dict =  {
                "id":self.id,
                "name":self.name,
                "rating":self.rating,
                "prep_time":self.prep_time
                }
        if self.menu:
            return_dict['menu_id'] = self.menu_id
        return return_dict
    
    @classmethod
    def undictionfy(cls,response_body):
        try:
            new_brek = cls(
                name = response_body['name'],
                rating = response_body['rating'],
                prep_time = response_body['prep_time']
            )
        except KeyError:
            abort(make_response({"warning":"You must enter a name, rating and prep_time value"},404))
        return new_brek


