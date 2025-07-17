import sqlite3
import functools

# Configure logging (optional, for debugging)
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def with_db_connection(func):
    """Decorator to automatically handle database connection opening and closing."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            # Call the function with the connection as the first argument
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
            logging.info("Database connection closed.")
        return result
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

#### Fetch user by ID with automatic connection handling
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
    user = get_user_by_id(user_id=1)
    print(user)  # Should print (1, 'Alice', 30)