```python
#!/usr/bin/python3
import mysql.connector

def stream_users():
    """
    Generator function to stream rows from the user_data table one by one.
    Yields:
        dict: A dictionary containing user_id, name, email, and age for each row.
    """
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="",  # Replace with your MySQL password
            database="ALX_prodev"
        )
        
        cursor = connection.cursor(dictionary=True)  # Use dictionary cursor for dict output
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        
        # Yield each row one by one using a single loop
        for row in cursor:
            yield {
                'user_id': row['user_id'],
                'name': row['name'],
                'email': row['email'],
                'age': row['age']
            }
        
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return
```