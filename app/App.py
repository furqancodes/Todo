import threading
import datetime
import time
from db.connection import Database
from db.queries import create_table, insert_todo, get_todos, get_todo_by_id, update_todo, delete_todo_by_id
from enum import Enum

class Status(Enum):
    NOT_STARTED = 1
    IN_PROGRESS = 2
    COMPLETED = 3

status_names = {
    1: "Not Started",
    2: "In Progress",
    3: "Completed"
}

def create_todo(heading, description):
    insert_todo(heading, description, None, Status.NOT_STARTED.value, None, None)

def list_todo():
    todos_data = get_todos()
    if todos_data:
        for todo_data in todos_data:
            print(f"ID: {todo_data['id']}")
            print(f"Heading: {todo_data['heading']}")
            print(f"Description: {todo_data['description']}")
            print(f"Status: {status_names[todo_data['status']]}")
            print(f"Start Date: {todo_data['start_date']}")
            print(f"End Date: {todo_data['end_date']}")
            print(f"Reminder Time: {todo_data['reminder_time']}")
            print()
    else:
        print("No todo items found.")

def item_exists(todo_id):
    return get_todo_by_id(todo_id) is not None

def delete_todo(todo_id):
    if item_exists(todo_id):
        delete_todo_by_id(todo_id)
    else:
        print("Todo item not found.")
        raise(ValueError)

def set_reminder(todo_id, reminder_minutes):
    if item_exists(todo_id):
        reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=reminder_minutes)
        todo_data = get_todo_by_id(todo_id)
        update_todo(todo_data['id'], todo_data['heading'], todo_data['description'], reminder_time, todo_data['status'], todo_data['start_date'], todo_data['end_date'])
    else:
        print("Todo item not found.")

def update_todo_item(todo_id, new_heading, new_description):
    if item_exists(todo_id):
        todo_data = get_todo_by_id(todo_id)
        update_todo(todo_data['id'], new_heading, new_description, todo_data['reminder_time'], todo_data['status'], todo_data['start_date'], todo_data['end_date'])
    else:
        print("Todo item not found.")

def check_reminders():
    while True:
        current_time = datetime.datetime.now()
        todos_data = get_todos()
        for todo_data in todos_data:
            if todo_data['reminder_time'] and current_time >= todo_data['reminder_time']:
                print(f'Reminder for task "{todo_data["heading"]}" reached at {current_time.strftime("%Y-%m-%d %H:%M:%S")}.')
                update_todo(todo_data['id'], todo_data['heading'], todo_data['description'], None, todo_data['status'], todo_data['start_date'], todo_data['end_date'])
        time.sleep(60)  # Check every minute

def move_todo_item(todo_id):
    if item_exists(todo_id):
        todo_data = get_todo_by_id(todo_id)
        status = todo_data['status']
        if status != Status.COMPLETED.value:
            new_status = status + 1
            start_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") if new_status == Status.IN_PROGRESS.value else todo_data['start_date']
            end_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") if new_status == Status.COMPLETED.value else todo_data['end_date']
            update_todo(todo_data['id'], todo_data['heading'], todo_data['description'], todo_data['reminder_time'], new_status, start_date, end_date)
        else:
            print("Task is completed.")
    else:
        print("Todo item not found.")

def start_app():
    select_menu()

def select_menu():
    options = {
        'a': list_todo,
        'b': lambda: create_todo(input("Enter heading: "), input("Enter description: ")),
        'c': lambda: delete_todo(int(input("Enter Id of the todo item to delete: "))),
        'd': lambda: set_reminder(int(input("Enter Id of the task to add reminder: ")), int(input("Enter reminder time in minutes: "))),
        'e': lambda: update_todo_item(int(input("Enter Id of the todo item to update: ")), input("Enter new heading: "), input("Enter new description: ")),
        'f': lambda: move_todo_item(int(input("Enter Id of the task to move: ")))
    }
    while True:
        list_todo()
        selected_option = input("Select an option \na) List todo tasks\nb) Add todo task\nc) Delete todo task\nd) Set reminder to a todo\ne) Update todo task\nf) Move todo task\nPress any key to exit\n").lower()
        if selected_option in options:
            options[selected_option]()
        else:
            break

if __name__ == "__main__":
    Database.initialize()
    reminder_thread = threading.Thread(target=check_reminders, daemon=True)
    reminder_thread.start()
    create_table()
    start_app()
