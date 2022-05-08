from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint
#from api.task_api import Task, TaskDB

crud_lifter_blueprint = Blueprint('crud_lifter_blueprint', __name__)

@crud_lifter_blueprint.route("/", methods = ["GET", "POST"])
def home_page():

    return render_template("home-page.html")

@crud_lifter_blueprint.route("/new_member", methods=["POST"])
def member_creation():
    return render_template("new-member.html")