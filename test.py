import mysql.connector

# Establish the connection
connection = mysql.connector.connect(
    host="127.0.0.1",  # The IP address of the MySQL server
    user="root",       # The username for the database
    password="super123",       # The password for the database (if any, otherwise leave it empty)
    database="user_auth"  # The database name you want to use
)

# Check if the connection is successful
if connection.is_connected():
    print("Connected to the database")

    # Create a cursor object
    cursor = connection.cursor()

    # Execute a query
    cursor.execute("SELECT * FROM users WHERE email = 'lecturer@usth.edu.vn' AND password = 'password123' AND role = 'Lecturer';")

    # Fetch the results
    results = cursor.fetchall()

    print(results)

    # Close the cursor and connection
    cursor.close()
    connection.close()
else:
    print("Failed to connect to the database")
