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
        selectedOption = input("Select an option \na) List todo tasks\nb)Add todo task\nc)Delete todo task\nPress any key to exit\n")
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
        for todo,index in enumerate(todosList):
            print(f"{index})",todo)
        if runStartFunction:
            startApp()
        return None
    # function to delete todo
    def deleteTodo():
        listTodo()
        id = int(input('Enter id of the todo item to delete '))
        todosList.pop(id)
        listTodo(True)

    # function to goto start
    def startApp():
        selectMenu()
        if selectedOption.lower() == 'a':
            listTodo(True)
        elif selectedOption.lower() == 'b':
            createTodo()
        elif selectedOption.lower() == 'c':
            deleteTodo()
        else:
            return None
        return None
    startApp()
    return None
main()

