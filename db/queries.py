from sqlalchemy import MetaData, Table,insert,Column,Integer,String,TIMESTAMP,Boolean
from sqlalchemy.exc import SQLAlchemyError
from db.connection import Database

metadata = MetaData()

def get_or_create_todos_table():
    with Database() as connection:
        todos = Table('todos', metadata,
                      Column('id', Integer, primary_key=True, autoincrement=True),
                      Column('heading', String(255), nullable=False),
                      Column('description', String, nullable=True),
                      Column('reminder_time', TIMESTAMP, nullable=True),
                      Column('status', Integer, nullable=False),
                      Column('start_date', TIMESTAMP, nullable=True),
                      Column('end_date', TIMESTAMP, nullable=True),
                      Column('is_deleted', Boolean, default=False),
                      extend_existing=True)

        if not connection.dialect.has_table(connection, 'todos'):
            metadata.create_all(connection)
        else:
            metadata.reflect(bind=connection, only=['todos'])
    return todos

todos = get_or_create_todos_table()

def insert_todo(heading, description):
    with Database() as connection:
        try:
            query = insert(todos).values(heading=heading, description=description, status=1)
            connection.execute(query)
        except SQLAlchemyError as e:
            print(e)

def get_todos():
    with Database() as connection:
        try:
            query = todos.select().where(todos.c.is_deleted == False)
            result = connection.execute(query)
            rows = result.fetchall()
            columns =  result.keys()
            return [dict(zip(columns, row)) for row in rows]

        except SQLAlchemyError as e:
            print(e)
            return []

def get_todo_by_id(todo_id):
    with Database() as connection:
        try:
            query = todos.select().where(todos.c.id == todo_id, todos.c.is_deleted == False)
            result = connection.execute(query)
            row = result.fetchone()
            columns =  result.keys()

            return dict(zip(columns, row)) if row else None
        except SQLAlchemyError as e:
            print(e)
            return None

def update_todo(todo_id, heading, description, reminder_time, status, start_date, end_date):
    with Database() as connection:
        try:
            query = todos.update().where(todos.c.id == todo_id).values(
                heading=heading, description=description, reminder_time=reminder_time,
                status=status, start_date=start_date, end_date=end_date
            )
            connection.execute(query)
        except SQLAlchemyError as e:
            print(e)

def delete_todo_by_id(todo_id):
    with Database() as connection:
        try:
            query = todos.update().where(todos.c.id == todo_id).values(is_deleted=True)
            connection.execute(query)
        except SQLAlchemyError as e:
            print(e)
