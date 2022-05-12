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
    """
    Creates the database for flask app

    INPUT:
        config - values of individual's database configuration

    """
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"]
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"DROP DATABASE IF EXISTS {config['DATABASE']};")
    cursor.execute(f"CREATE DATABASE {config['DATABASE']};")
    cursor.execute(f"use {config['DATABASE']};")

    # Current working database is not fully normalized, with exercise_sets allowing duplicate entries
    # If we were to rework the test cases and database model functions, workouts should be formally foreign key
    # linked to weight_sets by date. 

    # Additional information in exercise_sets to allow sets of same weight on same machine at same day
    # could be another avenue of improving the database design. (i.e. timestamp with minutes, not just day)
    
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
            PRIMARY KEY (gym_id, workout_date),
            FOREIGN KEY (gym_id) REFERENCES gym_members(gym_id)
        );
    """ )

    cursor.execute( """
        CREATE TABLE exercise_sets
        (
            gym_id SMALLINT UNSIGNED,
            machine_name VARCHAR(100),
            exercise_date VARCHAR(100),
            reps TINYINT UNSIGNED,
            weight SMALLINT
            
        );
        """)

    cursor.close()
    conn.close()
    click.echo("DB Initialized")
