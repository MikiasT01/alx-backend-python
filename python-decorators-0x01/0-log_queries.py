import sqlite3
import functools
import logging

# Configure logging to write to a file (e.g., 'query.log')
logging.basicConfig(filename='query.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

#### Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the query from args (assuming it's the first positional argument)
        query = args[0] if args else kwargs.get('query', '')
        if query:
            logging.info(f"Executing query: {query}")
        # Execute the original function
        result = func(*args, **kwargs)
        return result
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### Fetch users while logging the query
if __name__ == "__main__":
    # Ensure users.db exists with a users table (create if needed)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
    conn.commit()
    conn.close()

    # Test the function
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)  # Should print empty list if no data, logged in query.log