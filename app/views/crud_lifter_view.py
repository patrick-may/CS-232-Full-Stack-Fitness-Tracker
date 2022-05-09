from flask import Blueprint, request, redirect, Flask
from flask import render_template, g, Blueprint
from flask_login import LoginManager
import click
from models.gym_member import Gym_Member, Gym_Member_DB
from models.weight_set import Weight_Set_DB, Weight_Set

crud_lifter_blueprint = Blueprint('crud_lifter_blueprint', __name__)

@crud_lifter_blueprint.route("/", methods = ["GET", "POST"])
def home_page():
    memberDB = Gym_Member_DB(g.mysql_db, g.mysql_cursor)

    display_data = memberDB.select_all_members()

    setDB = Weight_Set_DB(g.mysql_db, g.mysql_cursor)

    weight_data = setDB.select_all_exercises()

    return render_template("home-page.html", data=display_data, weight_data=weight_data)
    #return render_template("home-page.html", data=display_data)

"""
Incomplete login thing
@crud_lifter_blueprint("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        login_user(user)
        click.echo("Logged in successfully")
        next = Flask.request.args.get('next')

        if not is_safe_url(next):
            return Flask.abort(400)
        
        return 
"""


@crud_lifter_blueprint.route('/create_member')
def gather_member_info():
   return render_template("member-entry.html")

@crud_lifter_blueprint.route("/add_member", methods=["POST"])
def member_creation():
    new_member_name = request.form.get("member_name")
    new_member_age = request.form.get("member_age")
    new_member_sex = request.form.get("member_sex")

    new_member = Gym_Member(new_member_name, new_member_age, new_member_sex)
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

@crud_lifter_blueprint.route("/create_weight_set")
def gather_set_info():
    return render_template("weight-set-entry.html")

@crud_lifter_blueprint.route("/add_weight_set", methods=["POST"])
def set_creation():
    machine_name = request.form.get("machine_name")
    user_id = request.form.get("user_id")
    date = request.form.get("date")
    reps = request.form.get("reps")
    weight = request.form.get("weight")
    setDB = Weight_Set_DB(g.mysql_db, g.mysql_cursor)
    setDB.insert_weight_set(Weight_Set(machine_name, user_id, date, reps, weight))
    return redirect("/")