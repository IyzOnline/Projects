from django.db import models

# Create your models here.
class Behavior(models.Model):
    title = models.TextField(max_length=20)
    description = models.TextField(max_length=100)

class LogEntry(models.Model):
    pass