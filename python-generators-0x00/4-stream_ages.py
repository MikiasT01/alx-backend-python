```python
#!/usr/bin/python3
import mysql.connector

def stream_user_ages():
    """
    Generator function to yield user ages one by one from the user_data table.
    Yields:
        float: The age of each user.
    """
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="",  # Replace with your MySQL password
            database="ALX_prodev"
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        
        # Yield each age one by one using a single loop
        for row in cursor:
            yield row[0]
        
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return

def calculate_average_age():
    """
    Calculates the average age of users using the stream_user_ages generator.
    Prints:
        The average age in the format 'Average age of users: <average>'.
    Returns:
        float: The average age, or None if no users are found.
    """
    total_age = 0
    count = 0
    
    # Single loop to process ages from the generator
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        print("Average age of users: No users found")
        return None
    
    average = total_age / count
    print(f"Average age of users: {average:.2f}")
    return average

if __name__ == "__main__":
    calculate_average_age() 
```