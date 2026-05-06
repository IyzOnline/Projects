from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Behavior(models.Model):
    title = models.TextField(max_length=20)
    description = models.TextField(max_length=100)

    expected_metrics = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.title

class LogEntry(models.Model):
    date = models.DateTimeField(default=timezone.now)
    behavior = models.ForeignKey(
        Behavior,
        on_delete=models.CASCADE,
        related_name='logs'
    )

    quality = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ],
        help_text="Rate how it went from 0 to 5."
    )

    special_note = models.TextField(max_length=250)

    custom_metrics = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"{self.behavior.title} on {self.date}"