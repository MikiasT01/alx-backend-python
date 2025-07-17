import time
import sqlite3
import functools
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Global cache dictionary
query_cache = {}

# Decorator from Task 1 to handle database connections
def with_db_connection(func):
    """Decorator to automatically handle database connection opening and closing."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
            logging.info("Database connection closed.")
        return result
    return wrapper

#### Decorator to cache query results
def cache_query(func):
    """Decorator to cache database query results based on the query string."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Get the query from args or kwargs
        query = args[0] if args else kwargs.get('query', '')
        if not query:
            raise ValueError("No query provided for caching")

        # Check if result is in cache
        if query in query_cache:
            logging.info(f"Returning cached result for query: {query}")
            return query_cache[query]

        # Execute the function and cache the result
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        logging.info(f"Cached result for query: {query}")
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
if __name__ == "__main__":
    # Create users.db and users table if they don't exist
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
    cursor.execute("INSERT OR IGNORE INTO users (name, age) VALUES (?, ?)", ("Bob", 25))
    conn.commit()
    conn.close()

    # Test the function
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print("First call result:", users)  # Should print [(1, 'Alice', 30), (2, 'Bob', 25)]

    # Second call should use cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print("Second call result:", users_again)  # Should print the same, using cache