import mysql.connector
from mysql.connector import Error
import config
import os

def execute_sql_file(cursor, filename):
    """
    Read and execute SQL commands from a file.
    """
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return

    with open(filename, 'r') as file:
        sql_commands = file.read().split(';')
        for command in sql_commands:
            if command.strip():
                try:
                    cursor.execute(command)
                except Error as e:
                    print(f"Error executing command: {command[:50]}...")  # Print first 50 chars
                    print(f"MySQL Error: {e}")

def main():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )

        if connection.is_connected():
            print("Connected to MySQL Musician database!")

            # Create a cursor object
            with connection.cursor() as cursor:
                # Execute schema SQL file
                print("Creating schema...")
                execute_sql_file(cursor, 'schema.sql')
                connection.commit()
                print("Schema created successfully.")

                # Execute insert SQL file
                print("Inserting data...")
                execute_sql_file(cursor, 'insert.sql')
                connection.commit()
                print("Data inserted successfully.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            connection.close()
            print("The MySQL connection is closed")

if __name__ == '__main__':
    main()
