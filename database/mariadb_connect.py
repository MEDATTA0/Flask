from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

username = "admin"
password = "admin"
host = "localhost"
port = "3306"
database = "todosDBTest"

connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(connection_string)

#A session is a lightweight object used to interact with the database within a specific context.
# It's optional, but it can improve performance and simplify database transactions
# sessionLocal = sessionmaker(bind=engine)
#Always close the session when you're done to avoid resource leaks
#Consider using sessions for managing database transactions and improving code organization, especially for more complex operations.

if engine.connect():
    print("mariadb connected successfully")
