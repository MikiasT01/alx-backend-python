import asyncio
import aiosqlite

async def async_fetch_users():
    """Asynchronously fetch all users from the database."""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users():
    """Asynchronously fetch users older than 40 from the database."""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    """Run both fetch functions concurrently and print results."""
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All users:", users)
    print("Users older than 40:", older_users)

if __name__ == "__main__":
    # Create users.db and users table if they don't exist
    import sqlite3
    initial_conn = sqlite3.connect('users.db')
    cursor = initial_conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
    cursor.execute("INSERT OR IGNORE INTO users (name, age) VALUES (?, ?)", ("Bob", 45))
    cursor.execute("INSERT OR IGNORE INTO users (name, age) VALUES (?, ?)", ("Charlie", 20))
    initial_conn.commit()
    initial_conn.close()

    # Run the concurrent fetch
    asyncio.run(fetch_concurrently())