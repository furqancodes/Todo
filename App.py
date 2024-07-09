import threading
import datetime
import time

class Todo:
    def __init__(self, heading, description):
        self.heading = heading
        self.description = description
        self.reminder_time = None

    def __str__(self):
        return f"Heading: {self.heading}\nDescription: {self.description}"

def selectMenu():
    options = {
        'a': listTodo,
        'b': createTodo,
        'c': deleteTodo,
        'd': setReminder,
        'e': updateTodo
    }
    selected_option = input("Select an option \na) List todo tasks\nb) Add todo task\nc) Delete todo task\nd) Set reminder to a todo\ne) Update todo task\nPress any key to exit\n").lower()
    if selected_option in options:
        options[selected_option]()
    else:
        exit()

def createTodo():
    heading = input("Enter heading: ")
    description = input("Enter description: ")
    todo = Todo(heading, description)
    todosList.append(todo)
    startApp()

def listTodo():
    if todosList:
        for index, todo in enumerate(todosList):
            print(f"{index + 1}) {todo}")
    else:
        print("No todo items found.")
    startApp()

def deleteTodo():
    listTodo()
    try:
        id = int(input('Enter id of the todo item to delete: '))
        if 1 <= id <= len(todosList):
            todosList.pop(id - 1)
        else:
            print("Invalid id.")
    except ValueError:
        print("Please enter a valid number.")
    startApp()

def setReminder():
    listTodo()
    try:
        index = int(input("Enter Id of the task to add reminder: "))
        if 1 <= index <= len(todosList):
            reminder_minutes = int(input("Enter reminder time in minutes: "))
            reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=reminder_minutes)
            todosList[index - 1].reminder_time = reminder_time
            print(f'Reminder set for task with id {index} in {reminder_minutes} minutes.')
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter valid numbers.")
    startApp()

def updateTodo():
    listTodo()
    try:
        id = int(input('Enter id of the todo item to update: '))
        if 1 <= id <= len(todosList):
            new_heading = input("Enter new heading: ")
            new_description = input("Enter new description: ")
            todosList[id - 1].heading = new_heading
            todosList[id - 1].description = new_description
        else:
            print("Invalid id.")
    except ValueError:
        print("Please enter a valid number.")
    startApp()

def checkReminders():
    while True:
        current_time = datetime.datetime.now()
        for todo in todosList:
            if todo.reminder_time and current_time >= todo.reminder_time:
                print(f'Reminder for task "{todo.heading}" reached at {current_time.strftime("%Y-%m-%d %H:%M:%S")}.')
                todo.reminder_time = None  # Reset reminder once reached
        time.sleep(60)  # Check every minute

def startApp():
    selectMenu()

if __name__ == "__main__":
    todosList = []
    # Start a thread to check reminders in the background
    reminder_thread = threading.Thread(target=checkReminders, daemon=True)
    reminder_thread.start()
    startApp()
