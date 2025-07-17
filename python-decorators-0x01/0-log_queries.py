import sqlite3
import functools
from datetime import datetime
import logging

# Configure logging to write to a file with custom timestamp
logging.basicConfig(filename='query.log', level=logging.INFO,
                    format='%(message)s')

#### Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the query from args or kwargs
        query = args[0] if args else kwargs.get('query', '')
        if query:
            # Log with custom datetime timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logging.info(f"[{timestamp}] Executing query: {query}")
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
    # Create users.db and users table if they don't exist
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)''')
    # Add some test data
    cursor.execute("INSERT OR IGNORE INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
    cursor.execute("INSERT OR IGNORE INTO users (name, age) VALUES (?, ?)", ("Bob", 25))
    conn.commit()
    conn.close()

    # Test the function
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)  # Should print [(1, 'Alice', 30), (2, 'Bob', 25)]