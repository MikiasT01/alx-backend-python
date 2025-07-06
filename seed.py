```python
#!/usr/bin/python3
import mysql.connector
import csv
import uuid

def connect_db():
    """
    Connects to the MySQL database server.
    Returns:
        connection: MySQL connection object or None if connection fails.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password=""   # Replace with your MySQL password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    """
    Creates the ALX_prodev database if it does not exist.
    Args:
        connection: MySQL connection object.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

def connect_to_prodev():
    """
    Connects to the ALX_prodev database.
    Returns:
        connection: MySQL connection object or None if connection fails.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="",  # Replace with your MySQL password
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """
    Creates the user_data table if it does not exist.
    Args:
        connection: MySQL connection object.
    """
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def insert_data(connection, csv_file):
    """
    Inserts data from the CSV file into the user_data table if it does not exist.
    Args:
        connection: MySQL connection object.
        csv_file: Path to the CSV file containing user data.
    """
    try:
        cursor = connection.cursor()
        
        # Read CSV file
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            
            for row in csv_reader:
                user_id = str(uuid.uuid4())  # Generate UUID for user_id
                name = row[0]                # Name from CSV
                email = row[1]               # Email from CSV
                age = float(row[2])          # Age from CSV
                
                # Check if email already exists to avoid duplicates
                cursor.execute("SELECT email FROM user_data WHERE email = %s", (email,))
                if cursor.fetchone():
                    continue
                
                # Insert data
                insert_query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (user_id, name, email, age))
        
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    except FileNotFoundError:
        print(f"CSV file {csv_file} not found")
    except Exception as e:
        print(f"Unexpected error: {e}")
```