from db.connection import Database

def create_table():
    connection = Database.get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos (
         id SERIAL PRIMARY KEY,
        heading VARCHAR(255),
        description TEXT,
        reminder_time TIMESTAMP,
        status INTEGER,
        start_date TIMESTAMP,
        end_date TIMESTAMP,
        is_deleted BOOLEAN DEFAULT FALSE
    )
    """)
    connection.commit()
    cursor.close()
    Database.return_connection(connection)

def insert_todo(heading, description, reminder_time, status, startDate, endDate):
    connection = Database.get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO todos (heading, description, reminder_time, status, start_date, end_date) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (heading, description, reminder_time, status, startDate, endDate))
    connection.commit()
    cursor.close()
    Database.return_connection(connection)

def get_todos():
    connection = Database.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM todos WHERE is_deleted = FALSE")
    columns = [desc[0] for desc in cursor.description]  # Get column names
    rows = cursor.fetchall()
    todos = [dict(zip(columns, row)) for row in rows]
    cursor.close()
    Database.return_connection(connection)
    return todos

def get_todo_by_id(todo_id):
    connection = Database.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
    row = cursor.fetchone()
    if row:
        columns = [desc[0] for desc in cursor.description]
        todo = dict(zip(columns, row))
    else:
        todo = None
    cursor.close()
    Database.return_connection(connection)
    return todo

def update_todo(todo_id, heading, description, reminder_time, status, startDate, endDate):
    connection = Database.get_connection()
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE todos
    SET heading = %s, description = %s, reminder_time = %s, status = %s, start_date = %s, end_date = %s
    WHERE id = %s
    """, (heading, description, reminder_time, status, startDate, endDate, todo_id))
    connection.commit()
    cursor.close()
    Database.return_connection(connection)

def delete_todo_by_id(todo_id):
    connection = Database.get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE todos SET is_deleted = TRUE WHERE id = %s", (todo_id,))
    connection.commit()
    cursor.close()
    Database.return_connection(connection)
