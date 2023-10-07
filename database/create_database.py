from database import create_connection, execute_query
from mysql.connector import Error



def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


connection = create_connection()
create_database_query = "CREATE DATABASE ozon_parsing_db DEFAULT CHARACTER SET utf8 "
create_database(connection, create_database_query)

create_table = """
CREATE TABLE IF NOT EXISTS exchange (
  id INT AUTO_INCREMENT, 
  date DATE 
  future_dollar TEXT NOT NULL, 
  age INT, 
  gender TEXT, 
  nationality TEXT, 
  PRIMARY KEY (id)
) ENGINE = InnoDB
"""

execute_query(connection, create_users_table)

create_posts_table = """
CREATE TABLE IF NOT EXISTS posts (
  id INT AUTO_INCREMENT, 
  title TEXT NOT NULL, 
  description TEXT NOT NULL, 
  user_id INTEGER NOT NULL, 
  FOREIGN KEY fk_user_id (user_id) REFERENCES users(id), 
  PRIMARY KEY (id)
) ENGINE = InnoDB
"""