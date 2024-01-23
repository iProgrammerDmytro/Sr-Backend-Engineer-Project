from django.db import models


class DatabaseCredentials(models.Model):
    hostname = models.CharField(max_length=255)
    db_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    port = models.IntegerField(default=5432)
    db_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.db_type} Database - {self.db_name} at {self.hostname} (User: {self.username})"
