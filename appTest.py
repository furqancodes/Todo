import unittest
from app import createTodo, deleteTodo, setReminder, updateTodo, todosList

class TestTodoApp(unittest.TestCase):

    def setUp(self):
        todosList.clear()  # Clear the list before each test

    def test_create_todo_success(self):
        createTodo("Test Task", "Test Description")
        self.assertEqual(len(todosList), 1)
        self.assertEqual(todosList[0].heading, "Test Task")
        self.assertEqual(todosList[0].description, "Test Description")

    def test_delete_todo_success(self):
        createTodo("Test Task", "Test Description")
        deleteTodo(0)
        self.assertEqual(len(todosList), 0)

    def test_delete_todo_invalid_index(self):
        createTodo("Test Task", "Test Description")
        with self.assertRaises(ValueError):
            deleteTodo(1)  # Index 1 is invalid because we only have one item at index 0

    def test_set_reminder_success(self):
        createTodo("Test Task", "Test Description")
        setReminder(0, 5)
        self.assertIsNotNone(todosList[0].reminder_time)

    def test_update_todo_success(self):
        createTodo("Test Task", "Test Description")
        updateTodo(0, "Updated Task", "Updated Description")
        self.assertEqual(todosList[0].heading, "Updated Task")
        self.assertEqual(todosList[0].description, "Updated Description")

if __name__ == '__main__':
    unittest.main()
