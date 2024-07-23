import unittest
from app.App import createTodo, deleteTodo, setReminder, updateTodo, moveTodoItem,Status
from db.queries import get_todos, get_todo_by_id, delete_todo_by_id
from db.connection import Database

class TestTodoApp(unittest.TestCase):

    def setUp(self):
        # Clear the database before each test
        Database.initialize()
        todos = get_todos()
        for todo in todos:
            delete_todo_by_id(todo['id'])

    def test_create_todo_success(self):
        createTodo("Test Task", "Test Description")
        todos = get_todos()
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0]['heading'], "Test Task")
        self.assertEqual(todos[0]['description'], "Test Description")

    def test_delete_todo_success(self):
        createTodo("Test Task", "Test Description")
        todos = get_todos()
        todo_id = todos[0]['id']
        deleteTodo(todo_id)
        todos = get_todos()
        self.assertEqual(len(todos), 0)

    def test_delete_todo_invalid_id(self):
        createTodo("Test Task", "Test Description")
        invalid_id = 9999  # An ID that doesn't exist
        with self.assertRaises(ValueError):
            deleteTodo(invalid_id)

    def test_set_reminder_success(self):
        createTodo("Test Task", "Test Description")
        todos = get_todos()
        todo_id = todos[0]['id']
        setReminder(todo_id, 5)
        todo = get_todo_by_id(todo_id)
        self.assertIsNotNone(todo['reminder_time'])

    def test_update_todo_success(self):
        createTodo("Test Task", "Test Description")
        todos = get_todos()
        todo_id = todos[0]['id']
        updateTodo(todo_id, "Updated Task", "Updated Description")
        todo = get_todo_by_id(todo_id)
        self.assertEqual(todo['heading'], "Updated Task")
        self.assertEqual(todo['description'], "Updated Description")

    def test_move_status(self):
        createTodo('Test heading', "Test Description")
        todos = get_todos()
        todo_id = todos[0]['id']
        moveTodoItem(todo_id)
        todo = get_todo_by_id(todo_id)
        self.assertEqual(todo['status'], Status.IN_PROGRESS.value)

if __name__ == '__main__':
    unittest.main()
