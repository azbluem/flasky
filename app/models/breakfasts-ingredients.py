from app import db

class BreakfastIngredients(db.Model):
    __tablename__='breakfast_ingredients'
    breakfast_id = db.Column(db.Integer, db.ForeignKey('breakfast_id'), primary_key=True, nullable=False)
    # ingredients_id = db.Column(db.Integer, db.ForeignKey('ingredients_id'), primary_key=True, nullable=False)