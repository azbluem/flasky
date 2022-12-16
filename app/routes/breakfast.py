from flask import Blueprint, jsonify, abort, make_response, request
from app.models.breakfasts import Breakfast
from app import db

breakfast_bp = Blueprint("breakfast_bp", __name__, url_prefix="/breakfast")

# breakfasts = [Breakfast(1,"Eggs Benny", 4, 60),
#             Breakfast(2,"Orange", 2, 1),
#             Breakfast(3, "Nothing",0,0),
#             Breakfast(3,"Croissant",5,360)]

@breakfast_bp.route("", methods=["POST", "PUT"])
def add_brekky():
    request_body = request.get_json()  # type: ignore

    new_brekky = Breakfast.undictionfy(request_body)
    
    db.session.add(new_brekky)
    db.session.commit()

    return make_response(jsonify(f"{new_brekky.name} added to menu"),201)


@breakfast_bp.route("", methods=["GET"])
def get_menu():
    breakfast_list = []
    name_query = request.args.get("name")
    rating_query = request.args.get("rating")
    preptime_query = request.args.get("prep_time")
    if name_query:
        breakfasts = Breakfast.query.filter_by(name=name_query)
    elif rating_query:
        breakfasts = Breakfast.query.filter(Breakfast.rating>=rating_query).all()
    elif preptime_query:
        breakfasts = Breakfast.query.filter(Breakfast.prep_time<preptime_query).all()
    else:
        breakfasts = Breakfast.query.order_by(Breakfast.id).all()
    for option in breakfasts:
        breakfast_list.append(option.dictionfy())
    return make_response(jsonify(breakfast_list))

@breakfast_bp.route("/<brekky_id>", methods=["GET"])
def get_one_breakfast(brekky_id):
    brekky = validate_model(Breakfast,brekky_id)
    return make_response(brekky.dictionfy(),200)

@breakfast_bp.route("/<brekky_id>", methods=["PUT"])
def update_one_breakfast(brekky_id):
    brekky = validate_model(Breakfast,brekky_id)
    request_body = request.get_json()
    try:
        brekky.name = request_body["name"]
        brekky.rating = request_body["rating"]
        brekky.prep_time = request_body["prep_time"]
    except KeyError:
        return make_response(f"You need to input name, rating AND prep time"),400

    db.session.commit()

    return make_response(jsonify(f'Breakfast with ID {brekky_id} has been successfully updated'),202)

@breakfast_bp.route("/<brekky_id>", methods=["PATCH"])
def rerate_one_breakfast(brekky_id):
    brekky = validate_model(Breakfast,brekky_id)
    request_body = request.get_json()

    name_change = brekky_patch_helper(brekky,"name",request_body)
    rating_change = brekky_patch_helper(brekky,"rating",request_body)
    prep_change = brekky_patch_helper(brekky,"prep_time",request_body)
    upvote_change = brekky_patch_helper(brekky,"upvotes",request_body)
    if not name_change and not rating_change and not prep_change and not upvote_change:
        return make_response(jsonify('Please send valid information: name, rating or prep time. K thx <3'),418)
    db.session.commit()

    return make_response(jsonify(f'Breakfast with ID {brekky_id} has been successfully patched'),202)

def brekky_patch_helper(brekky, value, request_body):
    try:
        setattr(brekky, value, request_body[value])
    except KeyError:
        return None
    return True

@breakfast_bp.route("/<brekky_id>", methods=["DELETE"])
def eat_the_breakfast(brekky_id):
    brekky = validate_model(Breakfast,brekky_id)

    db.session.delete(brekky)
    db.session.commit()

    return make_response(jsonify(f'Breakfast with ID {brekky_id} has been successfully devoured'),202)

def validate_model(model,brekky_id):
    try:
        brekky_id = int (brekky_id)
    except ValueError:
        abort(make_response({"message": f"{brekky_id} is not a valid breakfast"},400))
    brekky = model.query.get(brekky_id)
    
    if not brekky:
        abort(make_response({"message":f"Sorry, {brekky_id} is not on the menu, have some tea!"},418))
    return brekky
