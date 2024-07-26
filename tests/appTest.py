import unittest
from unittest.mock import patch, MagicMock
from app.App import create_todo, list_todo, Status,delete_todo,set_reminder,update_todo_item,move_todo_item
from io import StringIO
import datetime
from freezegun import freeze_time


class TestTodoApp(unittest.TestCase):

    @patch('db.queries.Database')
    def test_create_todo_success(self, mock_database):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_database.return_value.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        create_todo('Test Heading', 'Test Description')

        self.assertTrue(mock_cursor.execute.called)
        
        query, params = mock_cursor.execute.call_args[0]
        
        self.assertEqual(params, ('Test Heading', 'Test Description', None, Status.NOT_STARTED.value, None, None))
        
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('db.queries.Database')
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_todo_with_items(self, mock_stdout, mock_database):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_database.return_value.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            (1, 'Test Heading', 'Test Description', None, 1, None, None, False)
        ]
        mock_cursor.description = [
            ('id',), ('heading',), ('description',), ('reminder_time',), ('status',), ('start_date',), ('end_date',), ('is_deleted',)
        ]

        list_todo()

        output = mock_stdout.getvalue().strip()
        expected_output = (
            "ID: 1\n"
            "Heading: Test Heading\n"
            "Description: Test Description\n"
            "Status: Not Started\n"
            "Start Date: None\n"
            "End Date: None\n"
            "Reminder Time: None"
        )
        self.assertEqual(output, expected_output)

    @patch('db.queries.Database')
    def test_delete_todo_success(self, mock_database):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_database.return_value.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = {'id': 1}

        delete_todo(1)
        mock_cursor.execute.assert_called_with("UPDATE todos SET is_deleted = TRUE WHERE id = %s", (1,))
        mock_connection.commit.assert_called_once()
        self.assertEqual(mock_cursor.close.call_count, 2)
    
    @patch('db.queries.Database')
    @patch('sys.stdout', new_callable=StringIO)
    def test_delete_todo_by_unknown_id(self,mock_stdout,mock_database):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_database.return_value.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        self.assertRaises(ValueError,delete_todo,1)
        output = mock_stdout.getvalue().strip()
        expected_output = "Todo item not found."
        self.assertEqual(output, expected_output)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM todos WHERE id = %s", (1,))
        mock_connection.commit.assert_not_called()
        
    @patch('db.queries.Database')
    @freeze_time("2024-07-26 19:42:47.089679")
    def test_set_reminder_success(self, mock_database):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_database.return_value.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (1, 'Test Heading', 'Test Description', None, 1, None, None, False)
        mock_cursor.description = [
            ('id',), ('heading',), ('description',), ('reminder_time',), ('status',), ('start_date',), ('end_date',), ('is_deleted',)
        ]

        set_reminder(1, 10)
        reminder_time = datetime.datetime(2024, 7, 26, 19, 52, 47, 89679)
        
        mock_cursor.execute.assert_any_call("SELECT * FROM todos WHERE id = %s", (1,))
        mock_cursor.execute.assert_any_call(
            '\n        UPDATE todos\n        SET heading = %s, description = %s, reminder_time = %s, status = %s, start_date = %s, end_date = %s\n        WHERE id = %s\n        ',
            ('Test Heading', 'Test Description', reminder_time, 1, None, None, 1)
        )
        
        mock_connection.commit.assert_called_once()
        self.assertEqual(mock_cursor.close.call_count, 3)

    @patch('db.queries.Database')
    def test_update_todo_success(self, mock_database):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_database.return_value.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (1, 'Old Heading', 'Old Description', None, 1, None, None, False)
        mock_cursor.description = [
            ('id',), ('heading',), ('description',), ('reminder_time',), ('status',), ('start_date',), ('end_date',), ('is_deleted',)
        ]

        update_todo_item(1, 'New Heading', 'New Description')

        mock_cursor.execute.assert_any_call("SELECT * FROM todos WHERE id = %s", (1,))
        mock_cursor.execute.assert_any_call('\n        UPDATE todos\n        SET heading = %s, description = %s, reminder_time = %s, status = %s, start_date = %s, end_date = %s\n        WHERE id = %s\n        ', ('New Heading', 'New Description', None, 1, None, None, 1))
        
        
        mock_connection.commit.assert_called_once()
        self.assertEqual(mock_cursor.close.call_count, 3)

    @patch('db.queries.Database')
    @freeze_time("2024-07-26 19:42:47")
    def test_move_todo_item_success(self, mock_database):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_database.return_value.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (1, 'Test Heading', 'Test Description', None, Status.NOT_STARTED.value, None, None, False)
        mock_cursor.description = [
            ('id',), ('heading',), ('description',), ('reminder_time',), ('status',), ('start_date',), ('end_date',), ('is_deleted',)
        ]

        move_todo_item(1)
        
        mock_cursor.execute.assert_any_call("SELECT * FROM todos WHERE id = %s", (1,))
        mock_cursor.execute.assert_any_call('\n        UPDATE todos\n        SET heading = %s, description = %s, reminder_time = %s, status = %s, start_date = %s, end_date = %s\n        WHERE id = %s\n        ', ('Test Heading', 'Test Description', None, 2, '2024-07-26 19:42:47', None, 1))
        
        mock_connection.commit.assert_called_once()
        self.assertEqual(mock_cursor.close.call_count, 3)

    @patch('db.queries.Database')
    @patch('sys.stdout', new_callable=StringIO)
    def test_move_todo_item_completed(self, mock_stdout, mock_database):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_database.return_value.__enter__.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = (1, 'Test Heading', 'Test Description', None, Status.COMPLETED.value, None, None, False)
        mock_cursor.description = [
            ('id',), ('heading',), ('description',), ('reminder_time',), ('status',), ('start_date',), ('end_date',), ('is_deleted',)
        ]

        move_todo_item(1)
        
        output = mock_stdout.getvalue().strip()
        expected_output = "Task is completed."
        self.assertEqual(output, expected_output)
        mock_cursor.execute.assert_any_call("SELECT * FROM todos WHERE id = %s", (1,))
        self.assertEqual(mock_cursor.execute.call_count, 2)
        mock_connection.commit.assert_not_called()
        self.assertEqual(mock_cursor.close.call_count, 2)


if __name__ == '__main__':
    unittest.main()
