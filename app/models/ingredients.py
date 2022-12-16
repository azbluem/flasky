from app import db

class Ingredients(db.Model):
    ingredients_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    ingredient_name = db.Column(db.String)
    ingredient_quantity = db.Column(db.Integer)
    # breakfasts_items = db.relationship('Breakfast', back_populates='ingredients', secondary='breakfast_ingredients')
