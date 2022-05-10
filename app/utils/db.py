"""
Collection of functions to help establish the database
"""
import mysql.connector
import click
from flask.cli import with_appcontext


def init_app(app):
    app.cli.add_command(init_db)
    
# Connect to MySQL and the task database
def connect_db(config):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"],
        database=config["DATABASE"]
    )
    return conn


# Setup for the Database
#   Will erase the database if it exists
def init_db(config):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"]
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"DROP DATABASE IF EXISTS {config['DATABASE']};")
    cursor.execute(f"CREATE DATABASE {config['DATABASE']};")
    cursor.execute(f"use {config['DATABASE']};")
    #cursor.execute(
    #    f""" 
    #    CREATE TABLE tasks
    #    (
    #        id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
    #        description VARCHAR(50),
    #        creation_datetime timestamp,
    #        completed TINYINT(1),
    #        CONSTRAINT pk_todo PRIMARY KEY (id)
    #    );
    #    """
    #)
    #member table init
    cursor.execute(
        """ 
        CREATE TABLE gym_members
        (
            gym_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            name VARCHAR(100),
            creation_datetime timestamp,
            age TINYINT UNSIGNED, 
            sex CHAR(1),
            PRIMARY KEY (gym_id)
        ); """)

    cursor.execute( """
        CREATE TABLE workouts
        (
            gym_id SMALLINT UNSIGNED NOT NULL,
            workout_date VARCHAR(100),
            duration TINYINT,
            PRIMARY KEY (gym_id, workout_date)
        );
    """ )

    cursor.execute( """
        CREATE TABLE exercise_sets
        (
            gym_id SMALLINT UNSIGNED,
            machine_name VARCHAR(100),
            exercise_date VARCHAR(100),
            reps TINYINT UNSIGNED,
            weight SMALLINT,
            PRIMARY KEY (gym_id, machine_name, exercise_date)
            
        );
        """)

    cursor.close()
    conn.close()
    click.echo("DB Initialized")
