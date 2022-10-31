from flask import Blueprint, jsonify, abort, make_response, request
from app.models.breakfasts import Breakfast
from app import db

breakfast_bp = Blueprint("breakfast_bp", __name__, url_prefix="/breakfast")

# breakfasts = [Breakfast(1,"Eggs Benny", 4, 60),
#             Breakfast(2,"Orange", 2, 1),
#             Breakfast(3, "Nothing",0,0),
#             Breakfast(3,"Croissant",5,360)]

@breakfast_bp.route("", methods=["POST"])
def add_brekky():
    request_body = request.get_json()
    new_brekky = Breakfast(
        name = request_body["name"],
        rating = request_body["rating"],
        prep_time = request_body["prep_time"]
    )
    db.session.add(new_brekky)
    db.session.commit()

    return make_response(jsonify(f"{new_brekky.name} added to menu"),201)


@breakfast_bp.route("", methods=["GET"])
def get_menu():
    breakfast_names = []
    breakfasts = Breakfast.query.all()
    for option in breakfasts:
        breakfast_names.append(option.name)
    return jsonify(breakfast_names)

@breakfast_bp.route("/<brekky_id>", methods=["GET"])
def get_one_breakfast(brekky_id):
    brekky = validate_breakfast(brekky_id)
    
    return ({
            "name":brekky.name,
            "rating":brekky.rating,
            "prep time":brekky.prep_time
            },200)

@breakfast_bp.route("/<brekky_id>", methods=["PATCH"])
def update_one_breakfast(brekky_id):
    brekky = validate_breakfast(brekky_id)
    request_body = request.get_json()

    brekky.name = request_body["name"]
    brekky.rating = request_body["rating"]
    brekky.prep_time = request_body["prep time"]

    db.session.commit()

    return make_response(jsonify(f'Breakfast with ID {brekky_id} has been successfully updated'),202)

@breakfast_bp.route("/<brekky_id>", methods=["DELETE"])
def eat_the_breakfast(brekky_id):
    brekky = validate_breakfast(brekky_id)

    db.session.delete(brekky)
    db.session.commit()

    return make_response(jsonify(f'Breakfast with ID {brekky_id} has been successfully devoured'),202)

def validate_breakfast(brekky_id):
    try:
        brekky_id = int (brekky_id)
    except ValueError:
        abort(make_response({"message": f"{brekky_id} is not a valid breakfast"},400))
    brekky = Breakfast.query.get(brekky_id)
    
    if not brekky:
        abort(make_response({"message":f"Sorry, {brekky_id} is not on the menu, have some tea!"},418))
    return brekky
