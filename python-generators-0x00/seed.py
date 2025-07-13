import mysql.connector
import csv
import uuid
import os

def connect_db():
    """
    Connects to the MySQL database server.
    Returns a connection object or None if connection fails.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",  # Replace with your MySQL username
            password="your_password"  # Replace with your MySQL password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    """
    Creates the ALX_prodev database if it does not exist.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
        print("Database ALX_prodev created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

def connect_to_prodev():
    """
    Connects to the ALX_prodev database.
    Returns a connection object or None if connection fails.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",  # Replace with your MySQL username
            password="your_password",  # Replace with your MySQL password
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """
    Creates the user_data table if it does not exist.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(5,2) NOT NULL
            )
        """)
        cursor.close()
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def insert_data(connection, data):
    """
    Inserts data from the CSV file into the user_data table.
    Args:
        connection: MySQL connection object
        data: Path to the user_data.csv file
    """
    try:
        cursor = connection.cursor()
        with open(data, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                user_id, name, email, age = row
                # Validate UUID format
                try:
                    uuid.UUID(user_id)  # Ensure user_id is a valid UUID
                except ValueError:
                    print(f"Invalid UUID format for user_id: {user_id}")
                    continue
                # Insert data
                cursor.execute("""
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, name, email, float(age)))
        connection.commit()
        cursor.close()
        print("Data inserted successfully")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    except FileNotFoundError:
        print(f"CSV file {data} not found")
    except ValueError as ve:
        print(f"Error processing CSV data: {ve}")