import unittest
from unittest.mock import patch, MagicMock
from app.App import create_todo, list_todo, Status
from io import StringIO

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

if __name__ == '__main__':
    unittest.main()
