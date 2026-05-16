import unittest
from unittest.mock import patch, Mock
from utils.api_helpers import send_get_request, send_post_request


class TestApiHelpers(unittest.TestCase):

    @patch('utils.api_helpers.requests.get')
    def test_send_get_request_success(self, mock_get):
        mock_response = Mock()
        expected_data = {'status': 'success'}
        mock_response.json.return_value = expected_data
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        url = "https://example.com/api"
        result = send_get_request(url)

        self.assertEqual(result, expected_data)
        mock_get.assert_called_once_with(url, params=None, headers=None, timeout=10)

    @patch('utils.api_helpers.requests.get')
    def test_send_get_request_failure(self, mock_get):
        mock_get.side_effect = Exception("API failure")

        try:
            result = send_get_request("https://example.com/fail", retries=2)
            self.assertIsNone(result)
        except Exception:
            self.fail("send_get_request raised Exception unexpectedly!")

    @patch('utils.api_helpers.requests.post')
    def test_send_post_request_success(self, mock_post):
        mock_response = Mock()
        expected_data = {'result': 'ok'}
        mock_response.json.return_value = expected_data
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        url = "https://example.com/post"
        result = send_post_request(url, json_data={'key': 'value'})

        self.assertEqual(result, expected_data)
        mock_post.assert_called_once_with(
            url, data=None, json={'key': 'value'}, headers=None, timeout=10
        )

    @patch('utils.api_helpers.requests.post')
    def test_send_post_request_failure(self, mock_post):
        mock_post.side_effect = Exception("Timeout")

        try:
            result = send_post_request("https://example.com/postfail", retries=2)
            self.assertIsNone(result)
        except Exception:
            self.fail("send_post_request raised Exception unexpectedly!")


if __name__ == '__main__':
    unittest.main()
