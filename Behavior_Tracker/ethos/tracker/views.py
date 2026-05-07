from django.shortcuts import render, get_object_or_404

from .models import Behavior, LogEntry

from datetime import timedelta
from django.utils import timezone

# Create your views here.
def behavior_dashboard(request, behavior_id):
    behavior = get_object_or_404(Behavior, id=behavior_id)

    present = timezone.now()
    date_seven_days_ago = present - timedelta(days=7)
    
    past_week_logs = LogEntry.objects.filter(behavior, date__gte=date_seven_days_ago).order_by('date')

    quality_data = []
    date_data = []

    for log in past_week_logs:
        quality_data.append(log.quality)
        date_data.append(log.date.strftime('%b %d'))

    context = {
        'behavior': behavior,
        'quality_data_Y': quality_data,
        'date_data_X': date_data,
    }

    render(request, 'tracker/dashboard.html', context)
