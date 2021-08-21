import unittest
from unittest import mock
from api import API


class TestAPI(unittest.TestCase):

    api = None

    @classmethod
    def setUpClass(cls):
        cls.api = API()

    @classmethod
    def tearDownClass(cls):
        del cls.api

    #BeforeEach Test
    def setUp(self):
        self.mocked_session = mock.Mock(**{ "user": { "token": "blabla", "id": 5 }, "getToken.return_value": "blabla" })
        self.mocked_session.start()

    #AfterEach Test
    def tearDown(self):
        self.mocked_session.stop()

    #Session Mocking
    def test_session(self):
        self.assertEqual("blabla", self.mocked_session.getToken() )

    #Mock Passing to an Object
    def test_request_when_pageAndCountParametersAreNotNone_then_returnValueIsTrue_4(self):

        mock_something = mock.Mock(**{ "close.return_value": True})
        self.assertEqual(True, TestAPI.api.closer(mock_something))
        mock_something.close.assert_called_with()

    #Mock for Class Method of Module with Mock Patch
    @mock.patch('api.API.request')
    def test_init_api_request(self, mock_request):

        mock_request.return_value = True
        self.assertEqual(True, TestAPI.api.request(2, 5))
        mock_request.assert_called_once()

    #Mock Response Dictionary Example
    @mock.patch('requests.get')
    def test_request_when_pageAndCountParametersAreNotNone_then_returnValueIsTrue(self, mock_requests_get):

        dictionary = { "status_code": 200, "body": { "name": "Muhammed" }}
        mock_requests_get.return_value = dictionary
        response = TestAPI.api.request(2, 5)
        self.assertEqual(200, response['status_code'])
        self.assertEqual("Muhammed", response["body"]["name"] )
        mock_requests_get.assert_called_once()

    #Mock Response Object Example
    @mock.patch('requests.get')
    def test_request_when_pageAndCountParametersAreNotNone_then_returnValueIsTrue_2(self, mock_requests_get):

        mock_response = mock.Mock(**{ "status_code": 200, "body.return_value": { "name": "Muhammed" }})
        mock_requests_get.return_value = mock_response
        response = TestAPI.api.request(2, 5)
        self.assertEqual(200, response.status_code)
        self.assertEqual("Muhammed", response.body()["name"] )
        mock_requests_get.assert_called_with('https://jsonapi/articles?page=2&count=5')

    #Decorator Mocking
    @mock.patch('requests.get', return_value=mock.Mock(**{ "status_code": 200, "body.return_value": { "name": "Muhammed" }}))
    def test_request_when_pageAndCountParametersAreNotNone_then_returnValueIsTrue_21(self, mock_requests_get):

        response = TestAPI.api.request(2, 5)
        self.assertEqual(200, response.status_code)
        self.assertEqual("Muhammed", response.body()["name"] )
        mock_requests_get.assert_called_once()

    #Context Manager Mocking
    def test_request_when_pageAndCountParametersAreNotNone_then_returnValueIsTrue_212(self):

        with mock.patch('requests.get', return_value=mock.Mock(**{ "status_code": 200, "body.return_value": { "name": "Muhammed" }})) as mock_requests_get:
            response = TestAPI.api.request(2, 5)
            self.assertEqual(200, response.status_code)
            self.assertEqual("Muhammed", response.body()["name"] )
            mock_requests_get.assert_called_once()

    # Raising exceptions
    def test_request_when_pageParameterIsNone_then_raisesValueError(self):
        with self.assertRaises(ValueError):
            TestAPI.api.request(None, 5)

    # Raising exceptions
    def test_request_when_countParameterIsNone_then_raisesValueError(self):
        with self.assertRaises(ValueError):
            TestAPI.api.request(5, None)

if __name__ == '__main__':
    unittest.main()
