import sqlite3

class DatabaseConnection:
    """A context manager class to handle database connection opening and closing."""
    
    def __init__(self, db_name):
        """Initialize with the database file name."""
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the database connection, handling any exceptions."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    # Create users.db and users table if they don't exist
    initial_conn = sqlite3.connect('users.db')
    cursor = initial_conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
    cursor.execute("INSERT OR IGNORE INTO users (name, age) VALUES (?, ?)", ("Bob", 25))
    initial_conn.commit()
    initial_conn.close()

    # Use the context manager to fetch and print users
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print("Query results:", users)  # Should print [(1, 'Alice', 30), (2, 'Bob', 25)]