import unittest
from unittest.mock import patch, MagicMock
from db.queries import insert_todo, delete_todo_by_id, todos,update_todo
from app.App import check_reminders, move_todo_item,set_reminder
from datetime import datetime,timedelta

class TestTodoApp(unittest.TestCase):

    @patch('db.queries.Database.get_connection')
    def test_insert_todo(self, mock_get_connection):
        mock_connection = MagicMock()
        mock_get_connection.return_value = mock_connection

        heading = "Test Heading"
        description = "Test Description"

        insert_todo(heading, description)

        self.assertTrue(mock_connection.execute.called)
        actual_query = mock_connection.execute.call_args[0][0]

        self.assertIn('INSERT INTO todos', str(actual_query))
        self.assertIn('heading', str(actual_query))
        self.assertIn('description', str(actual_query))
        self.assertIn('status', str(actual_query))
        self.assertTrue(mock_connection.execute.call_args[0][0].is_insert)
        self.assertEqual(actual_query.compile().params['heading'], heading)
        self.assertEqual(actual_query.compile().params['description'], description)
        self.assertEqual(actual_query.compile().params['status'], 1)

    @patch('db.queries.Database.get_connection')
    @patch('db.queries.get_todo_by_id')
    def test_delete_todo_by_id(self, mock_get_todo_by_id, mock_get_connection):
        mock_connection = MagicMock()
        mock_get_connection.return_value = mock_connection

        todo_id = 2

        mock_get_todo_by_id.return_value = {
            'id': 2,
            'heading': 'Test Heading',
            'description': 'Test Description',
            'status': 1,
            'is_deleted': False
        }

        delete_todo_by_id(todo_id)

        self.assertTrue(mock_connection.execute.called)
        self.assertTrue(mock_connection.execute.call_args[0][0].is_update)
        actual_query = mock_connection.execute.call_args[0][0]
        print(actual_query,"actual")
        print(str(actual_query),"str")
        self.assertIn('UPDATE todos', str(actual_query))
        self.assertIn('SET is_deleted', str(actual_query))
        self.assertIn('WHERE todos.id = :id', str(actual_query))
        self.assertEqual(actual_query.compile().params['id_1'], todo_id)
        self.assertEqual(actual_query.compile().params['is_deleted'], True)

    
    @patch('db.queries.Database.get_connection')
    @patch('db.queries.get_todo_by_id') 
    def test_update_todo(self, mock_get_todo_by_id, mock_get_connection):
        mock_connection = MagicMock()
        mock_get_connection.return_value = mock_connection

        todo_id = 3
        new_heading = "Updated Heading"
        new_description = "Updated Description"

        mock_get_todo_by_id.return_value = {
            'id': todo_id,
            'heading': 'Old Heading',
            'description': 'Old Description',
            'reminder_time': None,
            'status': 1,
            'start_date': None,
            'end_date': None,
            'is_deleted': False
        }

        update_todo(todo_id, new_heading, new_description, None, 1, None, None)

        self.assertTrue(mock_connection.execute.called)
        self.assertTrue(mock_connection.execute.call_args[0][0].is_update)
        actual_query = mock_connection.execute.call_args[0][0]

        self.assertIn('UPDATE todos', str(actual_query))
        self.assertIn('SET heading=:heading, description=:description', str(actual_query))
        self.assertIn('WHERE todos.id = :id', str(actual_query))
        self.assertEqual(actual_query.compile().params['heading'], new_heading)
        self.assertEqual(actual_query.compile().params['description'], new_description)
        self.assertEqual(actual_query.compile().params['id_1'], todo_id)

    @patch('db.queries.Database.get_connection')
    @patch('app.App.get_todo_by_id')
    def test_move_todo_item(self, mock_get_todo_by_id, mock_get_connection):
        mock_connection = MagicMock()
        mock_get_connection.return_value = mock_connection

        todo_id = 4
        mock_get_todo_by_id.return_value = {
            'id': todo_id,
            'heading': 'Test Heading',
            'description': 'Test Description',
            'status': 1,  # Not Started
            'reminder_time': None,
            'start_date': None,
            'end_date': None,
            'is_deleted': False
        }

        move_todo_item(todo_id)

        self.assertTrue(mock_connection.execute.called)
        self.assertTrue(mock_connection.execute.call_args[0][0].is_update)
        actual_query = mock_connection.execute.call_args[0][0]

        self.assertIn('UPDATE todos', str(actual_query))
        self.assertIn('status=:status, start_date=:start_date', str(actual_query))
        self.assertIn('WHERE todos.id = :id', str(actual_query))
        self.assertEqual(actual_query.compile().params['status'], 2)  # In Progress
        self.assertEqual(actual_query.compile().params['id_1'], todo_id)
        self.assertIsNotNone(actual_query.compile().params['start_date'])
    @patch('db.queries.Database.get_connection')
    @patch('app.App.get_todo_by_id')
    def test_set_reminder(self, mock_get_todo_by_id, mock_get_connection):
        mock_connection = MagicMock()
        mock_get_connection.return_value = mock_connection

        todo_id = 5
        reminder_minutes = 30
        reminder_time = datetime.now() + timedelta(minutes=reminder_minutes)

        mock_get_todo_by_id.return_value = {
            'id': todo_id,
            'heading': 'Test Heading',
            'description': 'Test Description',
            'status': 1,  # Not Started
            'reminder_time': None,
            'start_date': None,
            'end_date': None,
            'is_deleted': False
        }

        set_reminder(todo_id, reminder_minutes)

        self.assertTrue(mock_connection.execute.called)
        self.assertTrue(mock_connection.execute.call_args[0][0].is_update)
        actual_query = mock_connection.execute.call_args[0][0]

        self.assertIn('UPDATE todos', str(actual_query))
        self.assertIn('reminder_time=:reminder_time', str(actual_query))
        self.assertIn('WHERE todos.id = :id', str(actual_query))
        self.assertAlmostEqual(actual_query.compile().params['reminder_time'], reminder_time, delta=timedelta(seconds=1))
        self.assertEqual(actual_query.compile().params['id_1'], todo_id)
    
if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    unittest.main()
