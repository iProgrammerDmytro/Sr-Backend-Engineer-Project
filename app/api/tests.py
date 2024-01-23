from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase

from unittest.mock import patch, MagicMock

from .models import DatabaseCredentials


class DatabaseCredentialsModelTest(TestCase):

    def setUp(self):
        DatabaseCredentials.objects.create(
            hostname='localhost',
            db_name='testdb',
            username='testuser',
            password='testpass',
            port=5432,
            db_type='PostgreSQL'
        )

    def test_str_representation(self):
        """
        Test the __str__ method of DatabaseCredentials model.
        """
        credentials = DatabaseCredentials.objects.get(db_name='testdb')
        expected_str = f"PostgreSQL Database - testdb at localhost (User: testuser)"
        self.assertEqual(str(credentials), expected_str)


class DatabaseCredentialsViewTest(APITestCase):

    def test_create_database_credentials(self):
        """
        Ensure we can create a new database credentials object.
        """
        url = reverse(
            'databasecredentials-list')
        data = {
            'hostname': 'localhost',
            'db_name': 'testdb',
            'username': 'testuser',
            'password': 'testpass',
            'port': 5432,
            'db_type': 'PostgreSQL'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DatabaseCredentials.objects.count(), 1)
        self.assertEqual(
            DatabaseCredentials.objects.get().db_name, data['db_name']
        )


class DatabaseSchemaViewTest(APITestCase):

    def setUp(self):
        DatabaseCredentials.objects.create(
            hostname='localhost',
            db_name='testdb',
            username='testuser',
            password='testpass',
            port=5432,
            db_type='PostgreSQL'
        )

    @patch('psycopg2.connect')
    def test_get_schema_success(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            ('test_table', 'column1', 'varchar'),
        ]
        url = reverse('database-schema')
        response = self.client.get(url + '?db_name=testdb')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TableSearchViewTest(APITestCase):

    def setUp(self):
        DatabaseCredentials.objects.create(
            hostname='localhost',
            db_name='testdb',
            username='testuser',
            password='testpass',
            port=5432,
            db_type='PostgreSQL'
        )

    @patch('psycopg2.connect')
    def test_table_search_exists(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = [True]
        mock_cursor.fetchall.return_value = [
            ('column1', 'varchar', 'YES', None)]

        url = reverse('table-search')
        response = self.client.get(
            url + '?db_name=testdb&table_name=existing_table')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('columns', response.data)

    @patch('psycopg2.connect')
    def test_table_search_not_exists(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = [False]

        url = reverse('table-search')
        response = self.client.get(
            url + '?db_name=testdb&table_name=nonexistent_table')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('psycopg2.connect')
    def test_table_search_missing_parameters(self, mock_connect):
        url = reverse('table-search')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
