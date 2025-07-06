```python
#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator function to fetch rows from the user_data table in batches.
    Args:
        batch_size (int): Number of rows to fetch per batch.
    Yields:
        list: A list of dictionaries, each containing user_id, name, email, and age.
    """
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="",  # Replace with your MySQL password
            database="ALX_prodev"
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        
        # Fetch rows in batches using a single loop
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:  # Break if no more rows
                break
            yield [
                {
                    'user_id': row['user_id'],
                    'name': row['name'],
                    'email': row['email'],
                    'age': row['age']
                } for row in batch
            ]
        
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return

def batch_processing(batch_size):
    """
    Processes batches of users, filtering those over 25 years old.
    Args:
        batch_size (int): Number of rows to process per batch.
    Yields:
        dict: A dictionary containing user_id, name, email, and age for users over 25.
    """
    # Loop 1: Iterate over batches from stream_users_in_batches
    for batch in stream_users_in_batches(batch_size):
        # Loop 2: Iterate over rows in the batch
        for user in batch:
            if user['age'] > 25:
                yield user
```