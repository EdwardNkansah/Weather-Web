import unittest
from flask import Flask
from weather_app import app


class TestWeatherApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_index_route_with_valid_data(self):
        response = self.app.post('/', data={'country': 'Country', 'location_name': 'Location'})
        self.assertEqual(response.status_code, 200)
        # Add more assertions to validate the response content

    def test_index_route_with_invalid_data(self):
        response = self.app.post('/', data={'country': 'Invalid', 'location_name': 'Invalid'})
        self.assertEqual(response.status_code, 200)
        # Add assertions to verify that the error message is displayed correctly

    def test_index_route_with_empty_data(self):
        response = self.app.post('/', data={})
        self.assertEqual(response.status_code, 200)
        # Add assertions to verify that the error message is displayed correctly

    def test_index_route_with_get_request(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # Add assertions to validate the response content

if __name__ == '__main__':
    unittest.main()