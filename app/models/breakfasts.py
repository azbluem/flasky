from app import db

class Breakfast(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    rating = db.Column(db.Float)
    prep_time = db.Column(db.Integer)

    def dictionfy(self):
        return {
                "id":self.id,
                "name":self.name,
                "rating":self.rating,
                "prep_time":self.prep_time
                }
    def undictionfy(self,response_body):
        new_breakfast=Breakfast(
            name = response_body['name'],
            rating = response_body['rating'],
            prep_time = response_body['prep_time']
        )
        return new_breakfast

