from flask import Blueprint, jsonify, abort, make_response, request
from app.models.menu import Menu
from app.models.breakfasts import Breakfast
from app.routes.breakfast import validate_model
from app import db

menu_bp = Blueprint("menu_bp", __name__, url_prefix="/menu")

@menu_bp.route('', methods=['POST'])
def instance_menu():
    response_body = request.get_json()
    new_menu = Menu(
        resto=response_body['resto'],
        meal=response_body['meal']
    )
    db.session.add(new_menu)
    db.session.commit()
    
    return make_response(f'Menu with ID {new_menu.menu_id} was added',200)

@menu_bp.route('', methods=['GET'])
def get_all_menus():
    menus = Menu.query.all()
    return_list = [menu.dictionfy() for menu in menus]
    return make_response(jsonify(return_list),200)

@menu_bp.route('/<menu_id>/breakfasts',methods=['PUT','PATCH'])
def add_breakfasts_to_menus(menu_id):
    menu = validate_model(Menu,menu_id)
    response_body = request.get_json()
    for brek_id in response_body['brekky_ids']:
        brekky = validate_model(Breakfast,brek_id)
        brekky.menu = menu
        brekky.menu_id = menu.menu_id
    
    db.session.commit()

    return_dict = menu.dictionfy()
    breakfast_name_list = []
    for item in menu.breakfasts:
        breakfast_name_list.append(item.name)
    return_dict['breakfasts'] = breakfast_name_list

    return make_response(jsonify(return_dict),200)

@menu_bp.route('/<menu_id>/breakfasts',methods=['GET'])
def get_breks_on_menu(menu_id):
    menu = validate_model(Menu,menu_id)
    return_list = [item.dictionfy() for item in menu.breakfasts]

    return make_response(jsonify(return_list),200)