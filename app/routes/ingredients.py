from flask import Blueprint, jsonify, abort, make_response, request
from app.models.ingredients import Ingredients
from app import db

ingredient_bp = Blueprint("ingredient_bp", __name__, url_prefix="/ingredients")
