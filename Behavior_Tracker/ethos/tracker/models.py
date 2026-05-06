from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

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

    class Meta:
        # Q: why does Meta not need "()" or "(self)"?
        # A: Typing "Meta()" is valid, but is unidiotmatic.
        # Unidiomatic - fancy term meaning how it was designed failed to use Python's features and conventions
        # Also, it is not a method, so it does not need "(self)".

        ordering = ['-date']
        indexes = [
            models.Index(fields=['behavior', '-date'], name='behavior_date_idx'),
            models.Index(fields=['-date'], name='date_only_idx')
        ]


    def clean(self):
        # From what I've learned, the reason why super.clean() should be called here
        # is for future proofing because (1) the devs of Django might change the currently
        # empty clean method and (2) because I might create a Mixin class that LogEntry could
        # inherit from someday.
        super().clean()

        expected_metrics = self.behavior.expected_metrics
        actual_metrics = self.custom_metrics

        # Verify if all expected metrics defined under specific Behavior are present 
        for key in expected_metrics:
            if key not in actual_metrics:
                raise ValidationError(f"Missing required metric '{key}' for {self.behavior.title}")
            
        # Verify that there are no rogue metrics under actual metrics
        for key in actual_metrics:
            if key not in expected_metrics:
                raise ValidationError(f"An invalid metric was added: {key}")
            
        # Verify that the provided metrics have the correct type
        for key, expected_type in expected_metrics.items():
            value = actual_metrics[key]

            if expected_type == 'integer' and not isinstance(key, int):
                raise ValidationError(f"{key} must be of type 'int', instead got: {type(value).__name__}")

            if expected_type == "string" and not isinstance(key, str):
                raise ValidationError(f"{key} must be of type 'str', instead got: {type(value).__name__}")

    def __str__(self):
        return f"{self.behavior.title} on {self.date}"