from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint
#from api.task_api import Task, TaskDB
from models.gym_member import Gym_Member, Gym_Member_DB

crud_lifter_blueprint = Blueprint('crud_lifter_blueprint', __name__)

@crud_lifter_blueprint.route("/", methods = ["GET", "POST"])
def home_page():
    memberDB = Gym_Member_DB(g.mysql_db, g.mysql_cursor)

    display_data = memberDB.select_all_members()
    
    return render_template("home-page.html", data=display_data)

@crud_lifter_blueprint.route('/create_member')
def gather_member_info():
   return render_template("member-entry.html")

@crud_lifter_blueprint.route("/add_member", methods=["POST"])
def member_creation():
    new_member_name = request.form.get("member_name")
    new_member_age = request.form.get("member_age")
    new_member_sex = request.form.get("member_sex")

    new_member = Gym_Member(new_member_name, 0, new_member_age, new_member_sex)
    add_db = Gym_Member_DB(g.mysql_db, g.mysql_cursor)

    add_db.insert_individual_member(new_member)

    return redirect("/")

@crud_lifter_blueprint.route('/delete_member')
def member_deletion():
    return render_template("member-deletion.html")

@crud_lifter_blueprint.route("/remove_account", methods=["POST"])
def remove_member():
    user_id = request.form.get("member_id")
    delete_db = Gym_Member_DB(g.mysql_db, g.mysql_cursor)

    delete_db.delete_member(user_id)
    return redirect("/")
