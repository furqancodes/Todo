import threading
import datetime
import time
def main():
    #intialising variables ,functions and classes
    todosList=[]
    #todo class to create seprate objects
    class Todo:
        def __init__(self, heading, description):
            self.heading = heading
            self.description = description

        def __str__(self):
            return f"Heading: {self.heading}/nDescription: ({self.description})"
    # function to display menu and select option
    def selectMenu():
        # selectedOption is global so it can be accessed by other functions
        global selectedOption
        selectedOption = input("Select an option \na) List todo tasks\nb)Add todo task\nc)Delete todo task\nd)Set reminder to a todo\nPress any key to exit\n")
        return None
    # function to create todo item
    def createTodo():
        heading = input("Enter heading: ")
        description = input("Enter description: ")
        todo = Todo(heading,description)
        todosList.append(todo)
        startApp()
        return None
    # function to display all todos
    def listTodo(runStartFunction=False):
        for index,todo in enumerate(todosList):
            print(f"{index + 1})",todo)
        if runStartFunction:
            startApp()
        return None
    # function to delete todo
    def deleteTodo():
        listTodo()
        id = int(input('Enter id of the todo item to delete '))
        todosList.pop(id - 1)
        listTodo(True)
    #function to set reminder
    def setReminder():
        listTodo()
        index =int(input("Enter Id of the task to add reminder: "))
        reminder_minutes = int(input("Enter reminder time in minutes: "))
        if index >= 1 and index <= len(todosList):
            reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=reminder_minutes)
            todosList[index-1]["reminder_time"] = reminder_time
            print(f'Reminder set for task with id {index} in {reminder_minutes} minutes.')
        else:
            print("Invalid task number.")
        startApp()

    def checkReminders():
        while True:
            current_time = datetime.datetime.now()
            for todo in todosList:
                if todo["reminder_time"] and current_time >= todo["reminder_time"]:
                    print(f'Reminder for task "{todo["task"]}" reached at {current_time.strftime("%Y-%m-%d %H:%M:%S")}.')
                    todo["reminder_time"] = None  # Reset reminder once reached
            time.sleep(60)  # Check every minute
    # Start a thread to check reminders in the background
    reminder_thread = threading.Thread(target=checkReminders, daemon=True)
    reminder_thread.start()
    # function to goto start
    def startApp():
        selectMenu()
        if selectedOption.lower() == 'a':
            listTodo(True)
        elif selectedOption.lower() == 'b':
            createTodo()
        elif selectedOption.lower() == 'c':
            deleteTodo()
        elif selectedOption.lower() == 'd':
            setReminder()
        else:
            return None
        return None
    startApp()
    return None
main()

