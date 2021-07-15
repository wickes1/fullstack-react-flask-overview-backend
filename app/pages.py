from flask import Blueprint, render_template, jsonify, g, redirect, url_for
from .models import *
from app import db

page = Blueprint('page', __name__)


# @page.route('/')
# def login_page():
#     return render_template("login.html")


# @page.route("/profile")
# def profile():
#     if not g.user:
#         return redirect(url_for("/"))

#     return render_template("profile.html")
