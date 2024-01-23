from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import NotFound

import psycopg2
import psycopg2.extras

from .serializers import DatabaseCredentialsSerializer
from .models import DatabaseCredentials


class DatabaseCredentialsView(generics.CreateAPIView):
    serializer_class = DatabaseCredentialsSerializer


class DatabaseSchemaView(APIView):
    def get(self, request):
        db_name = request.query_params.get('db_name')
        if not db_name:
            return Response({"error": "Database name is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            credentials = DatabaseCredentials.objects.get(db_name=db_name)
        except DatabaseCredentials.DoesNotExist:
            raise NotFound(detail="Database credentials not found.")

        conn = psycopg2.connect(
            dbname=credentials.db_name,
            user=credentials.username,
            password=credentials.password,
            host=credentials.hostname
        )
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute("""
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position;
        """)
        schema_info = cur.fetchall()

        formatted_schema = self.format_schema(schema_info)

        return Response({
            "database_name": credentials.db_name,
            "schema": formatted_schema
        })

    def format_schema(self, schema_info):
        schema = {}
        for table_name, column_name, data_type in schema_info:
            if table_name not in schema:
                schema[table_name] = []
            schema[table_name].append(
                {"column_name": column_name, "data_type": data_type})
        return schema


class TableSearchView(APIView):
    def get(self, request):
        db_name = request.query_params.get('db_name')
        table_name = request.query_params.get('table_name')

        if not db_name or not table_name:
            return Response({"error": "Database name and table name are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            credentials = DatabaseCredentials.objects.get(db_name=db_name)
        except DatabaseCredentials.DoesNotExist:
            raise NotFound(detail="Database credentials not found.")

        try:
            conn = psycopg2.connect(
                dbname=credentials.db_name,
                user=credentials.username,
                password=credentials.password,
                host=credentials.hostname,
                port=credentials.port
            )
            cur = conn.cursor()
            # Check if the table exists
            cur.execute(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = %s);", (table_name,))
            exists = cur.fetchone()[0]

            if not exists:
                return Response({"error": "Table does not exist."}, status=status.HTTP_404_NOT_FOUND)

            # Query to get column details of the table
            cur.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns
                    WHERE table_schema = 'public' AND table_name = %s
                    ORDER BY ordinal_position;
                """, (table_name,))
            columns = cur.fetchall()
            cur.close()
            conn.close()

            formatted_columns = [{"column_name": col[0], "data_type": col[1],
                                  "is_nullable": col[2], "default": col[3]} for col in columns]

            return Response({"table_name": table_name, "columns": formatted_columns})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
