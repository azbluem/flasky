from app import db

class Menu(db.Model):
    menu_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    resto = db.Column(db.String)
    meal = db.Column(db.String)
    breakfasts = db.relationship('Breakfast', back_populates='menu')

    def dictionfy(self):
        return {
                "id":self.menu_id,
                "resto":self.resto,
                "meal":self.meal
                }
    
    def give_breakfasts(self):
        return_list=[]
        for brek in self.breakfasts:
            return_list.append(brek.dictionfy())
        return return_list
    