import unittest
from unittest.mock import patch, MagicMock
from generate_image import generate_image

class TestSwarmUIGenerator(unittest.TestCase):
    
    @patch('requests.post')
    def test_generate_image_success(self, mock_post):
        # Mock Session Response
        mock_session_resp = MagicMock()
        mock_session_resp.json.return_value = {"session_id": "test_session_123"}
        mock_session_resp.raise_for_status.return_value = None
        
        # Mock Generation Response
        mock_gen_resp = MagicMock()
        mock_gen_resp.json.return_value = {
            "images": ["/View/local/raw/image1.png"]
        }
        mock_gen_resp.raise_for_status.return_value = None
        
        mock_post.side_effect = [mock_session_resp, mock_gen_resp]
        
        # We use a dummy URL
        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            generate_image("test prompt", "http://localhost:7801", "test-model")
            
            # Check if second call was the generation call
            self.assertEqual(mock_post.call_count, 2)
            gen_payload = mock_post.call_args[1]['json']
            self.assertEqual(gen_payload['prompt'], "test prompt")
            self.assertEqual(gen_payload['session_id'], "test_session_123")

if __name__ == "__main__":
    unittest.main()
