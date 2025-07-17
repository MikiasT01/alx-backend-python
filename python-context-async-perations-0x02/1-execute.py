import sqlite3

class ExecuteQuery:
    """A context manager class to execute a database query and manage the connection."""
    
    def __init__(self, db_name, query, param):
        """Initialize with database file name, query, and parameter."""
        self.db_name = db_name
        self.query = query
        self.param = param
        self.conn = None
        self.result = None

    def __enter__(self):
        """Open the database connection, execute the query, and return the result."""
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute(self.query, (self.param,))
        self.result = cursor.fetchall()
        return self.result

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
    cursor.execute("INSERT OR IGNORE INTO users (name, age) VALUES (?, ?)", ("Charlie", 20))
    initial_conn.commit()
    initial_conn.close()

    # Use the context manager to execute the query and print results
    with ExecuteQuery('users.db', "SELECT * FROM users WHERE age > ?", 25) as result:
        print("Query results:", result)  # Should print [(1, 'Alice', 30)]