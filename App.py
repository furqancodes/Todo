import threading
import datetime
import time
import json
import os
from enum import Enum

class Status(Enum):
    NOT_STARTED = 1 
    IN_PROGRESS = 2
    COMPLETED = 3

status_names = {
        Status.NOT_STARTED:"Not Started",
        Status.IN_PROGRESS:"In Progress",
        Status.COMPLETED:"Completed"
    }
class Todo():
    def __init__(self, heading, description,reminder_time=None,status=Status.NOT_STARTED.value,startDate=None,endDate=None):
        self.heading = heading
        self.description = description
        self.reminder_time = reminder_time
        self.status=status
        self.startDate=startDate
        self.endDate=endDate

    def to_dict(self):
        return {
            "heading": self.heading,
            "description": self.description,
            "reminder_time": self.reminder_time.strftime("%Y-%m-%d %H:%M:%S") if self.reminder_time else None,
            "startDate":self.startDate,
            "endDate":self.endDate,
            "status":self.status,
        }
    def moveStatus(self):
        if self.status != Status.COMPLETED.value:
            self.status = self.status+1
            if self.status == Status.IN_PROGRESS.value:
                self.startDate = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            else:
                self.endDate = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            return None

        else:
            print("Task is completed.")
            return None

    @staticmethod
    def from_dict(data):
        reminder_time = datetime.datetime.strptime(data["reminder_time"], "%Y-%m-%d %H:%M:%S") if data["reminder_time"] else None
        startDate = data["startDate"] if data["startDate"] else None
        endDate = data["endDate"] if data["endDate"] else None
        status =  data["status"] if data["status"] else Status.NOT_STARTED.value
        return Todo(
            heading=data["heading"],
            description=data["description"],
            reminder_time=reminder_time,
            status=status,
            startDate=startDate,
            endDate=endDate
        )

todosList = []
storage_file = "todos.json"

def saveTodos():
    with open(storage_file, "w") as file:
        json.dump([todo.to_dict() for todo in todosList], file)

def loadTodos():
    global todosList
    if os.path.exists(storage_file):
        with open(storage_file, "r") as file:
            todos_data = json.load(file)
            todosList = [Todo.from_dict(todo_data) for todo_data in todos_data]

def createTodo(heading, description):
    todo = Todo(heading, description)
    todosList.append(todo)
    saveTodos()

def listTodo():
    if todosList:
        for index, todo in enumerate(todosList):
            print(f"{index+1})")
            print(f"Heading: {todo.heading}")
            print(f"Description: {todo.description}")
            print(f"Status: {status_names[todo.status]}")
            print(f"Start Date: {todo.startDate}")
            print(f"End Date: {todo.endDate}")
            print(f"Reminder Time: {todo.reminder_time}")
    else:
        print("No todo items found.")

def deleteTodo(index):
    if 0 <= index < len(todosList):
        todosList.pop(index)
        saveTodos()
    else:
        raise ValueError("Invalid index.")

def setReminder(index, reminder_minutes):
    if 0 <= index < len(todosList):
        reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=reminder_minutes)
        todosList[index].reminder_time = reminder_time
        saveTodos()
    else:
        raise ValueError("Invalid index.")

def updateTodo(index, new_heading, new_description):
    if 0 <= index < len(todosList):
        todosList[index].heading = new_heading
        todosList[index].description = new_description
        saveTodos()
    else:
        raise ValueError("Invalid index.")

def checkReminders():
    while True:
        current_time = datetime.datetime.now()
        for todo in todosList:
            if todo.reminder_time and current_time >= todo.reminder_time:
                print(f'Reminder for task "{todo.heading}" reached at {current_time.strftime("%Y-%m-%d %H:%M:%S")}.')
                todo.reminder_time = None  # Reset reminder once reached
        time.sleep(60)  # Check every minute
def moveTodoItem(index):
    if 0 <= index < len(todosList):
        todosList[index].moveStatus()
        saveTodos()
    else:
        raise ValueError("Invalid index.")


def startApp():
    loadTodos()
    selectMenu()

def selectMenu():
    options = {
        'a': listTodo,
        'b': lambda: createTodo(input("Enter heading: "), input("Enter description: ")),
        'c': lambda: deleteTodo(int(input("Enter Id of the todo item to delete: ")) - 1),
        'd': lambda: setReminder(int(input("Enter Id of the task to add reminder: ")) - 1, int(input("Enter reminder time in minutes: "))),
        'e': lambda: updateTodo(int(input("Enter Id of the todo item to update: ")) - 1, input("Enter new heading: "), input("Enter new description: ")),
        'f': lambda: moveTodoItem(int(input("Enter Id of the task to move: ")) - 1)
    }
    while True:
        listTodo()
        selected_option = input("Select an option \na) List todo tasks\nb) Add todo task\nc) Delete todo task\nd) Set reminder to a todo\ne) Update todo task\nf) Move todo task\nPress any key to exit\n").lower()
        if selected_option in options:
            options[selected_option]()
        else:
            saveTodos()  # Save todos before exiting
            break

if __name__ == "__main__": 
    # Start a thread to check reminders in the background
    reminder_thread = threading.Thread(target=checkReminders, daemon=True)
    reminder_thread.start()
    startApp()
