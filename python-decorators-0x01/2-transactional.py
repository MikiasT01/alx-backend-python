import sqlite3
import functools
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

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

#### Decorator to manage transactions
def transactional(func):
    """Decorator to manage database transactions with commit or rollback."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            logging.info("Transaction committed successfully.")
            return result
        except Exception as e:
            conn.rollback()
            logging.error(f"Transaction rolled back due to error: {e}")
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

#### Update user's email with automatic transaction handling
if __name__ == "__main__":
    # Create users.db and users table if they don't exist
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, email TEXT)''')
    # Add some test data
    cursor.execute("INSERT OR IGNORE INTO users (name, age, email) VALUES (?, ?, ?)", ("Alice", 30, "alice@example.com"))
    conn.commit()
    conn.close()

    # Test the function
    try:
        update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
        # Verify the update
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE id = 1")
        print(cursor.fetchone())  # Should print ('Crawford_Cartwright@hotmail.com',)
        conn.close()
    except Exception as e:
        print(f"Update failed: {e}")