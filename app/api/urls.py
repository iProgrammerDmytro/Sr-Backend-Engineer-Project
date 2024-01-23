from django.urls import path

from .views import (
    DatabaseCredentialsView,
    DatabaseSchemaView,
    TableSearchView
)


urlpatterns = [
    path('db-credentials/', DatabaseCredentialsView.as_view(), name="databasecredentials-list"),
    path('db-schema/', DatabaseSchemaView.as_view(), name="database-schema"),
    path('search-table/', TableSearchView.as_view(), name="table-search"),
]
