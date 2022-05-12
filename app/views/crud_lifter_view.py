from flask import Blueprint, request, redirect, Flask
from flask import render_template, g, Blueprint
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import click
from models.gym_member import Gym_Member, Gym_Member_DB
from models.weight_set import Weight_Set, Weight_Set_DB
from models.workout import Workout, WorkoutDB

crud_lifter_blueprint = Blueprint('crud_lifter_blueprint', __name__)


@crud_lifter_blueprint.route("/")
def home():
    return render_template("home-page.html")


@crud_lifter_blueprint.route("/login", methods=["POST", "GET"])
def login():
    """Basic function that authenticates the login for the user.

    The user enter their login credentials and is then redirected 
    to their respective user page

    Returns:
        redirect: Redirected to the user page. 

    """
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        flash("Login Successful!")
        return redirect("/user")
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect("/user")

        return render_template("login.html")


@crud_lifter_blueprint.route("/user")
def user():
    """Function where the user is shown all the options available to them.

    If the person logging in is the administrator then they are redirected to
    the login page where they are given the administrator control options of 
    creating and/or deleting members.


    Returns:
        Redirect: Redictered to either user or administrator page.

    """
    gym_db = Gym_Member_DB(g.mysql_db, g.mysql_cursor)

    if "user" in session:
        user = session["user"]

        if user == "admin":
            user_list = gym_db.select_all_members()
            return render_template("admin.html", user=user, gym_member_list=user_list)

        username = gym_db.select_individual_member(user)[0]["name"]
        weight_db = Weight_Set_DB(g.mysql_db, g.mysql_cursor)
        user_sets = weight_db.select_user_exercises(user)
        workout_db = WorkoutDB(g.mysql_db, g.mysql_cursor)
        all_workouts = workout_db.select_all_workouts(user)
        return render_template("user.html", user=username, member_sets=user_sets, workout_list=all_workouts)

    else:
        flash("You are not logged in")
        return redirect("/login")


@crud_lifter_blueprint.route("/logout")
def logout():
    """Basic function that simply logouts the user.


    Returns:
        Redirects: Send the user back to the login page
    """
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}", "info")
    session.pop("user", None)
    return redirect("/")


@crud_lifter_blueprint.route('/create_member')
def gather_member_info():
    """Returns front-end page to gather member information

    Returns:
        Redirect: web the member information is gathered.

    """
    return render_template("member-entry.html")


@crud_lifter_blueprint.route("/add_member", methods=["POST"])
def member_creation():
    """Function which leads to front-end page where the administrator 
    creates the entry for a new member.

    Returns:
        redirect: Returns to the admin page.

    """
    new_member_name = request.form.get("member_name")
    new_member_age = request.form.get("member_age")
    new_member_sex = request.form.get("member_sex")

    new_member = Gym_Member(new_member_name, new_member_age, new_member_sex)
    add_db = Gym_Member_DB(g.mysql_db, g.mysql_cursor)

    add_db.insert_individual_member(new_member)

    return redirect("/user")


@crud_lifter_blueprint.route('/delete_member')
def member_deletion():
    """Function the redirects the admin to delete a member.

    Returns:
        redirect: Returns the member deletion page.

    """
    return render_template("member-deletion.html")


@crud_lifter_blueprint.route("/remove_account", methods=["POST"])
def remove_member():
    """Function which connects the front-end to the back-end applications.

    Permitting the admin to remove members from the database. 

    Returns:
        redirect: Redirects the admin to their respective page.
    """
    user_id = request.form.get("member_id")
    delete_db = Gym_Member_DB(g.mysql_db, g.mysql_cursor)
    delete_db.delete_member(user_id)
    return redirect("/user")


@crud_lifter_blueprint.route("/update_member")
def member_update():
    """Function that redirects the admin to update member information.


    Returns:
        redirect: Sends the admin to the update page.
    """
    return render_template("member-update.html")


@crud_lifter_blueprint.route("/revise_member", methods=["POST"])
def member_revise():
    """Functions which connects the member update front-end to the back-end.

    Returns:
        redirect: Redirects the admin to their respective user page.
    """
    revise_id = request.form.get("member_id")
    new_member = Gym_Member(request.form.get("member_name"), request.form.get(
        "member_age"), request.form.get("member_sex"))
    update_db = Gym_Member_DB(g.mysql_db, g.mysql_cursor)
    update_db.update_member_info(revise_id, new_member)
    return redirect("/user")


@crud_lifter_blueprint.route("/create_workout")
def gather_workout_info():
    """Function that redirects the user to the enter workout data page.

    Returns:
        redirect: Sends the user to the enter workout values page.

    """
    if "user" not in session:
        redirect("/login")

    user = session["user"]
    weight_db = Weight_Set_DB(g.mysql_db, g.mysql_cursor)
    gym_db = Gym_Member_DB(g.mysql_db, g.mysql_cursor)
    user_sets = weight_db.select_all_exercises()
    username = gym_db.select_individual_member(user)[0]["name"]
    return render_template("workout-home.html", user=username, member_sets=user_sets)


@crud_lifter_blueprint.route("/add_workout", methods=["POST"])
def insert_workout():
    """Function connects the front-end to the back-end when the user inputs the 
    data for the workout.


    Returns:
        redirect: sends the user back to the user page after the workout is inserted.
    """
    if "user" in session:
        user_id = session["user"]
    else:
        user_id = 0

    workout_date = request.form.get("date")
    workout_duration = request.form.get("duration")
    exercises_list = []

    b = request.form
    machine_names = b.getlist("machine_name")
    reps = b.getlist("reps")
    weight = b.getlist("weight")

    for x in range(len(machine_names)):
        exercises_list.append(Weight_Set(
            machine_names[x], user_id, workout_date, reps[x], weight[x]))

    db = WorkoutDB(g.mysql_db, g.mysql_cursor)
    new_workout = Workout(user_id, workout_date,
                          workout_duration, exercises_list)
    db.insert_workout(new_workout)

    return redirect("/user")


@crud_lifter_blueprint.route("/create_weight_set")
def gather_set_info():
    """Function redirects the user to the create set template.

    Returns:
        redirect: sends the user to enter weight set page.

    """
    return render_template("weight-set-entry.html")


@crud_lifter_blueprint.route("/add_weight_set", methods=["POST"])
def set_creation():
    """Example function with types documented in the docstring.


    Returns:
        redirect: sends the user back to the user page after the set is added.
    """
    machine_name = request.form.get("machine_name")
    if "user" in session:
        user_id = session["user"]
    else:
        user_id = 0

    date = request.form.get("date")
    reps = request.form.get("reps")
    weight = request.form.get("weight")
    setDB = Weight_Set_DB(g.mysql_db, g.mysql_cursor)
    setDB.insert_weight_set(Weight_Set(
        machine_name, user_id, date, reps, weight))
    return redirect("/user")


@crud_lifter_blueprint.route("/delete_weight_set")
def set_remove():
    """Function redirects the user to the delete weight template.

    Returns:
        redirect: sends the user to the delete weigth template.

    """
    return render_template("weight-set-delete.html")


@crud_lifter_blueprint.route("/remove_weight_set", methods=["POST"])
def set_deletion():
    """Function connects the front-end with the back-end so it can 
    remove the desired weigth set.

    Returns:
        redirect: sends the user back to user page once the desired set 
        is removed.
    """

    if "user" in session:
        user_id = session["user"]
    else:
        user_id = 0

    machine_name = request.form.get("machine_name")
    date = request.form.get("date")
    setDB = Weight_Set_DB(g.mysql_db, g.mysql_cursor)
    setDB.delete_weight_set(machine_name, user_id, date)
    return redirect("/user")


@crud_lifter_blueprint.route("/revise_weight")
def revise_weight_set():
    """Function redirects the user update weight template.

    Returns:
        redirect: sends the user to update weight template.

    """
    return render_template("weight-set-update.html")


@crud_lifter_blueprint.route("/update_weight_set", methods=["POST"])
def update_weight_set():
    """Function connects the front-end with the back-end in terms helping the user  
    update their workout entry.

    Returns:
        redirect: sends the user back to user page after the weights are 
        updated

    """

    if "user" in session:
        user_id = session["user"]
    else:
        user_id = 0
    machine_name = request.form.get("machine_name")
    date = request.form.get("date")
    reps = request.form.get("reps")
    weight = request.form.get("weight")
    setDB = Weight_Set_DB(g.mysql_db, g.mysql_cursor)
    setDB.update_weight_set(Weight_Set(
        machine_name, user_id, date, reps, weight))
    return redirect("/user")


@crud_lifter_blueprint.route("/delete_workout")
def delete_workout():
    """Function redirects the user to the delete template file.

    Returns:
        redirect: sends the user to the delete workout page.

    """
    return render_template("workout-delete.html")


@crud_lifter_blueprint.route("/remove_workout", methods=["POST"])
def remove_workout():
    """function that connects front-end to back-end in terms giving the user 
    functionality to remove a workout.


    Returns:
        redirect: sends the user back to their user page 

    """
    if "user" in session:
        user_id = session["user"]
    else:
        user_id = 0

    workout_date = request.form.get("workout_date")
    db = WorkoutDB(g.mysql_db, g.mysql_cursor)
    db.delete_workout(user_id, workout_date)
    return redirect("/user")
