from flask import Blueprint
from flask import jsonify
from .models import *
from app import db

page = Blueprint('page', __name__)


@page.route('/')
def main_page():
    return 'Main Page'
