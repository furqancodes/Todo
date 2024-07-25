from db.connection import Database

def create_table():
    with Database() as connection:
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

def insert_todo(heading, description, reminder_time, status, startDate, endDate):
    with Database() as connection:
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO todos (heading, description, reminder_time, status, start_date, end_date) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (heading, description, reminder_time, status, startDate, endDate))
        connection.commit()
        cursor.close()

def get_todos():
    with Database() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM todos WHERE is_deleted = FALSE")
        columns = [desc[0] for desc in cursor.description]  # Get column names
        rows = cursor.fetchall()
        todos = [dict(zip(columns, row)) for row in rows]
        cursor.close()
    return todos

def get_todo_by_id(todo_id):
    with Database() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            todo = dict(zip(columns, row))
        else:
            todo = None
        cursor.close()
    return todo

def update_todo(todo_id, heading, description, reminder_time, status, startDate, endDate):
    with Database() as connection:
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE todos
        SET heading = %s, description = %s, reminder_time = %s, status = %s, start_date = %s, end_date = %s
        WHERE id = %s
        """, (heading, description, reminder_time, status, startDate, endDate, todo_id))
        connection.commit()
        cursor.close()

def delete_todo_by_id(todo_id):
    with Database() as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE todos SET is_deleted = TRUE WHERE id = %s", (todo_id,))
        connection.commit()
        cursor.close()
