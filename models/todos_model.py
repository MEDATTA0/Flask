from sqlalchemy import Column, Integer, String, Boolean, Date, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy_serializer import SerializerMixin

# from database.mariadb_connect import engine

username = "admin"
password = "admin"
host = "localhost"
port = "3306"
database = "todosDBTest"

connection_string = f"mariadb+pymysql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(connection_string)
if engine.connect():
    print("mariadb connected successfully")


# Create the class of database
class Base(DeclarativeBase):
    pass


# Defining the table
class Todo(Base, SerializerMixin):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer)
    title = Column(String(255), nullable=False)
    todo_description = Column(String(255))
    is_completed = Column(Boolean, default=False)
    due_date = Column(Date)
    created_at = Column(Date)
    updated_at = Column(Date)

    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}', is_completed='{self.is_completed}')>"


# Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
