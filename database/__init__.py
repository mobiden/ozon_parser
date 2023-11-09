import mysql.connector
from mysql.connector import Error
from settings import db_config, create_logs


def create_connection(host_name = db_config['host'],
                      user_name = db_config['user'],
                      user_password = db_config['password'],
                      db_name = db_config['database'],
                      port = db_config['port']
                                                           ):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            port=port,
        )
        create_logs("Connection to MySQL DB successful", False)
    except Exception as e:
        create_logs(f"The error '{e}' occurred", True)

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        create_logs("Query executed successfully", True)
    except Error as e:
        create_logs(f"The error '{e}' occurred", True)


#connection = create_connection()
create_users = """
INSERT INTO
  `users` (`name`, `age`, `gender`, `nationality`)
VALUES
  ('James', 25, 'male', 'USA'),
  ('Leila', 32, 'female', 'France'),
  ('Brigitte', 35, 'female', 'England'),
  ('Mike', 40, 'male', 'Denmark'),
  ('Elizabeth', 21, 'female', 'Canada');
"""
#execute_query(connection, create_users)



