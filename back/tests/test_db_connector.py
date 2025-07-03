import unittest
from unittest.mock import mock_open, patch
from dataclasses import dataclass
from utility.db_connector import DbConnector

@dataclass
class Dummy:
    name: str
    age: int

class TestDbConnector(unittest.TestCase):

    def setUp(self):
        # Datos de ejemplo del JSON
        self.fake_json = '[{"id": 0, "name": "Alice", "age": 30}]'

    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    def test_read_from_json(self, mock_file):
        db = DbConnector("fake.json", "id")
        self.assertEqual(db.content, [])
        mock_file.assert_called_with("fake.json", "r")

    @patch("builtins.open", new_callable=mock_open, read_data='[]')
    def test_insert_into_table(self, mock_file):
        # El write se llamará en _try_commit_else_rollback
        mock_file().write = lambda x: None

        db = DbConnector("fake.json", "id")
        dummy = Dummy(name="Bob", age=25)
        success = db.insert_into_table("id", dummy)
        self.assertTrue(success)
        self.assertEqual(len(db.content), 1)
        self.assertEqual(db.content[0]['name'], "Bob")

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 0, "name": "Alice", "age": 30}]')
    def test_update_by_key(self, mock_file):
        mock_file().write = lambda x: None

        db = DbConnector("fake.json", "id")
        dummy = Dummy(name="Updated", age=40)
        updated = db.update_by_key(dummy, "id", 0)
        self.assertTrue(updated)
        self.assertEqual(db.content[0]['name'], "Updated")

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 0, "name": "Alice", "age": 30}]')
    def test_get_one_by_attribute(self, mock_file):
        db = DbConnector("fake.json", "id")
        item = db.get_one_by_attribute("name", "Alice")
        self.assertIsNotNone(item)
        self.assertEqual(item['name'], "Alice")

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 0, "name": "Alice", "age": 30}]')
    def test_get_all_by_attribute(self, mock_file):
        db = DbConnector("fake.json", "id")
        items = db.get_all_by_attribute("name", "Alice")
        self.assertEqual(len(items), 1)

if __name__ == '__main__':
    unittest.main()
