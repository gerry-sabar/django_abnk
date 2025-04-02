import requests
from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient
from myinfo.client import MyInfoPersonalClientV4

class SingpassCallbackTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_callback(self):
        test_code = "dummy-test-code"
        response = self.client.get(f"/callback?code={test_code}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "callback received", "code": test_code})

class SingpassAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch.object(MyInfoPersonalClientV4, 'get_authorise_url') 
    def test_get_authorise_url(self, mock_get_authorise_url):
        mock_url = "http://test.mock.singpass"
        mock_get_authorise_url.return_value = mock_url
        response = self.client.get("/")
        result = response.json()        

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"url": "http://test.mock.singpass", "state": result['state']})

    @patch.object(MyInfoPersonalClientV4, 'retrieve_resource') 
    def test_person_data_success(self, mock_retrieve_resource):
        data = {'auth_code': 'test_data', 'auth_state': 'test_state'}
        mock_retrieve_resource.return_value = "dummy data"
        response = self.client.post("/", data, format='json')
        self.assertEqual(response.status_code, 200)

    @patch.object(MyInfoPersonalClientV4, 'retrieve_resource') 
    def test_person_data_double_retrieve(self, mock_retrieve_resource):
        data = {'auth_code': 'test_data', 'auth_state': 'test_state'}
        mock_retrieve_resource.side_effect = requests.exceptions.HTTPError("401 Client Error: Unauthorized for url:  https://test.api.myinfo.gov.sg/com/v4/token")
        response = self.client.post("/", data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "401 Client Error: Unauthorized for url:  https://test.api.myinfo.gov.sg/com/v4/token"})

    def test_person_data_not_json_request(self):
        data = {'oauth_code': 'test_data', 'oauth_state': 'test_value'}
        response = self.client.post("/", data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "Request is not JSON"})

    def test_person_data_empty_auth_state(self):
        data = {'auth_code': 'test_data'}
        response = self.client.post("/", data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"auth_state": ["auth_state is required"]})

    def test_person_data_empty_auth_code(self):
        data = {'auth_state': 'test_data'}
        response = self.client.post("/", data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"auth_code": ["auth_code is required"]})

