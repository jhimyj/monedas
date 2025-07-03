import unittest
from unittest.mock import patch
from utility.env_loader import EnvLoader

class TestEnvLoader(unittest.TestCase):

    @patch('utility.env_loader.load_dotenv')
    @patch.dict('os.environ', {'MY_SECRET': 'abc123'})
    def test_get_env_var_exists(self, mock_load_dotenv):
        env_loader = EnvLoader()
        value = env_loader.get('MY_SECRET')
        self.assertEqual(value, 'abc123')
        # Verifica que load_dotenv se haya llamado al crear instancia
        mock_load_dotenv.assert_called_once()

    @patch('utility.env_loader.load_dotenv')
    @patch.dict('os.environ', {}, clear=True)
    def test_get_env_var_missing(self, mock_load_dotenv):
        env_loader = EnvLoader()
        with self.assertRaises(Exception) as context:
            env_loader.get('MY_SECRET')
        self.assertIn("Couldnt find env variable", str(context.exception))

if __name__ == '__main__':
    unittest.main()
