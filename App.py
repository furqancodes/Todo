import threading
import datetime
import time
import random
import string
import os
import signal
class Todo:
    def __init__(self, heading, description):
        self.heading = heading
        self.description = description
        self.reminder_time = None

    def __str__(self):
        return f"Heading: {self.heading}\nDescription: {self.description}"

todosList = []

def createTodo(heading, description):
    todo = Todo(heading, description)
    todosList.append(todo)

def listTodo():
    if todosList:
        for index, todo in enumerate(todosList):
            print(f"{index + 1}) {todo}")
    else:
        print("No todo items found.")

def deleteTodo(index):
    if 0 <= index < len(todosList):
        todosList.pop(index)
    else:
        raise ValueError("Invalid index.")

def setReminder(index, reminder_minutes):
    if 0 <= index < len(todosList):
        reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=reminder_minutes)
        todosList[index].reminder_time = reminder_time
    else:
        raise ValueError("Invalid index.")

def updateTodo(index, new_heading, new_description):
    if 0 <= index < len(todosList):
        todosList[index].heading = new_heading
        todosList[index].description = new_description
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

def startApp():
    selectMenu()

def selectMenu():

    options = {
        'a': listTodo,
        'b': lambda: createTodo(input("Enter heading: "), input("Enter description: ")),
        'c': lambda: deleteTodo(int(input("Enter id of the todo item to delete: ")) - 1),
        'd': lambda: setReminder(int(input("Enter Id of the task to add reminder: ")) - 1, int(input("Enter reminder time in minutes: "))),
        'e': lambda: updateTodo(int(input("Enter id of the todo item to update: ")) - 1, input("Enter new heading: "), input("Enter new description: "))
    }
    while True:
        selected_option = input("Select an option \na) List todo tasks\nb) Add todo task\nc) Delete todo task\nd) Set reminder to a todo\ne) Update todo task\nPress any key to exit\n").lower()
        if selected_option in options:
            options[selected_option]()
        else:
            break    
# def fileTest(): 
#     while True:
#         time.sleep(10)
#         pid = os.getpid()
#         print(pid,"filtest") 
#         x = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
#         f = open(x, "x")
# def sigKillFunc():
#     os.kill(pid, signal.SIGKILL) 

if __name__ == "__main__": 
    # Start a thread to check reminders in the background
    reminder_thread = threading.Thread(target=checkReminders, daemon=True)
    reminder_thread.start()
    # fileThread = threading.Thread(target=fileTest,daemon=True)
    # fileThread.start()
    startApp()
