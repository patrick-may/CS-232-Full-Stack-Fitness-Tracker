"""
Collection of functions to help establish the database
"""
import mysql.connector


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
        f""" 
        CREATE TABLE members
        (
            gym_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            creation_datetime timestamp,
            age TINYINT UNSIGNED, 
            PRIMARY KEY (gym_i
        );
        """
    )
    cursor.close()
    conn.close()
