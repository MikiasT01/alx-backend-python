import time
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

#### Decorator to retry on failure
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    last_exception = e
                    attempt_num = attempt + 1
                    if attempt_num == retries:
                        logging.error(f"Max retries ({retries}) reached. Last error: {e}")
                        raise
                    logging.warning(f"Attempt {attempt_num} failed with {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
            raise last_exception  # Should not reach here due to raise in loop
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)  # Override default delay to 1 as per call
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    # Simulate a transient error on first attempt
    if not hasattr(fetch_users_with_retry, 'attempt_count'):
        fetch_users_with_retry.attempt_count = 0
    fetch_users_with_retry.attempt_count += 1
    if fetch_users_with_retry.attempt_count == 1:
        raise sqlite3.OperationalError("Simulated transient error")
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### Attempt to fetch users with automatic retry on failure
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

    # Reset attempt count for testing
    if hasattr(fetch_users_with_retry, 'attempt_count'):
        del fetch_users_with_retry.attempt_count

    # Test the function
    try:
        users = fetch_users_with_retry()
        print(users)  # Should print [(1, 'Alice', 30), (2, 'Bob', 25)] after retries
    except Exception as e:
        print(f"Failed to fetch users: {e}")