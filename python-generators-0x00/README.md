ALX Backend Python: Generators Module
About the Project
This project introduces advanced usage of Python generators to efficiently handle large datasets, process data in batches, and simulate real-world scenarios involving live updates and memory-efficient computations. The tasks focus on leveraging Python’s yield keyword to implement generators that provide iterative access to data, promoting optimal resource utilization and improving performance in data-driven applications.
Learning Objectives
By completing this project, you will:

Master Python Generators: Learn to create and utilize generators for iterative data processing, enabling memory-efficient operations.
Handle Large Datasets: Implement batch processing and lazy loading to work with extensive datasets without overloading memory.
Simulate Real-world Scenarios: Develop solutions to simulate live data updates and apply them to streaming contexts.
Optimize Performance: Use generators to calculate aggregate functions like averages on large datasets, minimizing memory consumption.
Apply SQL Knowledge: Use SQL queries to fetch data dynamically, integrating Python with databases for robust data management.

Requirements

Proficiency in Python 3.x.
Understanding of yield and Python’s generator functions.
Familiarity with SQL and database operations (MySQL and SQLite).
Basic knowledge of database schema design and data seeding.
Ability to use Git and GitHub for version control and submission.

Database Setup
To set up the MySQL database for Tasks 0 and 1:

Install MySQL on your system.
Ensure the mysql-connector-python library is installed:pip install mysql-connector-python


Update the connect_db and connect_to_prodev functions in seed.py and the connection parameters in 0-stream_users.py with your MySQL username and password.
Place the user_data.csv file in the python-generators-0x00 directory.
Run the 0-main.py script to set up the database and populate it with data:./0-main.py


Run the 1-main.py script to test the generator:./1-main.py



Sample user_data.csv (not provided, but assumed structure based on table schema):
name,email,age
Dan Altenwerth Jr.,Molly59@gmail.com,67
Glenda Wisozk,Miriam21@gmail.com,119
Daniel Fahey IV,Delia.Lesch11@hotmail.com,49
Ronnie Bechtelar,Sandra19@yahoo.com,22
Alma Bechtelar,Shelly_Balistreri22@hotmail.com,102
Jonathon Jones,Jody.Quigley-Ziemann33@yahoo.com,116

Tasks
0. Getting started with Python generators
Objective: Create a generator that streams rows from an SQL database one by one.
Instructions:

Write a Python script seed.py that:
Sets up the MySQL database ALX_prodev with a user_data table containing:
user_id (Primary Key, UUID, Indexed)
name (VARCHAR, NOT NULL)
email (VARCHAR, NOT NULL)
age (DECIMAL, NOT NULL)


Populates the database with sample data from user_data.csv.


Implement the following functions:
connect_db(): Connects to the MySQL server.
create_database(connection): Creates the ALX_prodev database if it does not exist.
connect_to_prodev(): Connects to the ALX_prodev database.
create_table(connection): Creates the user_data table if it does not exist.
insert_data(connection, data): Inserts data from the CSV file into user_data, avoiding duplicates based on email.



Files:

Directory: python-generators-0x00
Files: seed.py, README.md

Sample Output (from 0-main.py):
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ('006bfede-724d-4cdd-a2a6-59700f40d0da', 'Glenda Wisozk', 'Miriam21@gmail.com', 119), ('006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'Daniel Fahey IV', 'Delia.Lesch11@hotmail.com', 49), ('00af05c9-0a86-419e-8c2d-5fb7e899ae1c', 'Ronnie Bechtelar', 'Sandra19@yahoo.com', 22), ('00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'Alma Bechtelar', 'Shelly_Balistreri22@hotmail.com', 102)]

1. Generator that streams rows from an SQL database
Objective: Create a generator that streams rows from an SQL database one by one.
Instructions:

Write a Python script 0-stream_users.py that implements a generator function stream_users() using the yield keyword.
The function should fetch rows one by one from the user_data table in the ALX_prodev database.
Use no more than one loop in the function.
The generator should yield each row as a dictionary with keys user_id, name, email, and age.

Files:

Directory: python-generators-0x00
Files: 0-stream_users.py, README.md

Sample Output (from 1-main.py):
{'user_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}
{'user_id': '006bfede-724d-4cdd-a2a6-59700f40d0da', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}
{'user_id': '006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'name': 'Daniel Fahey IV', 'email': 'Delia.Lesch11@hotmail.com', 'age': 49}
{'user_id': '00af05c9-0a86-419e-8c2d-5fb7e899ae1c', 'name': 'Ronnie Bechtelar', 'email': 'Sandra19@yahoo.com', 'age': 22}
{'user_id': '00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'name': 'Alma Bechtelar', 'email': 'Shelly_Balistreri22@hotmail.com', 'age': 102}
{'user_id': '01187f09-72be-4924-8a2d-150645dcadad', 'name': 'Jonathon Jones', 'email': 'Jody.Quigley-Ziemann33@yahoo.com', 'age': 116}

Instructions for Submission

Create or update the files in the python-generators-0x00 directory of the alx-backend-python repository.
Commit and push your changes to GitHub:git add python-generators-0x00/*.py python-generators-0x00/*.md
git commit -m "Add seed.py for database setup, 0-stream_users.py for generator, and update README for Tasks 0-1"
git push origin main


