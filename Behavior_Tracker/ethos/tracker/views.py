from django.shortcuts import render, get_object_or_404, redirect

from .models import Behavior, LogEntry
from .forms import BehaviorForm

from datetime import timedelta
from django.utils import timezone
import json

def home(request):
    behaviors = Behavior.objects.all()
    context = {'behaviors': behaviors}
    return render(request, 'tracker/home.html', context)

def behavior_dashboard(request, behavior_id):
    behavior = get_object_or_404(Behavior, id=behavior_id)

    present = timezone.now()
    date_seven_days_ago = present - timedelta(days=7)
    
    past_week_logs = LogEntry.objects.filter(behavior=behavior, date__gte=date_seven_days_ago).order_by('date')

    quality_data = []
    date_data = []

    for log in past_week_logs:
        quality_data.append(log.quality)
        date_data.append(log.date.strftime('%b %d'))

    context = {
        'behavior': behavior,
        'quality_data_Y': json.dumps(quality_data),
        'date_data_X': json.dumps(date_data),
    }

    return render(request, 'tracker/dashboard.html', context)

def create_behavior(request):
    if request.method == 'POST':
        form = BehaviorForm(request.POST)
        # request.POST is simply a QueryDict which is a Django object that contains the information
        # from the forms packaged by the browser and sent to the server. 

        # From what I understand, the BehaviorForm that inherits from forms.ModelForm returns
        # a Form Object that contains the dictionary of information passed as an argument to BehaviorForm. 

        if form.is_valid():
            form.save()
            # form.save() is the only time that a Behavior instance is created,
            
            return redirect('tracker:home')
            # what redirect returns is a HttpResponseRedirect object. What the object contains is simply the
            # status code 302, and the header for where it should redirect which in this case is '/tracker/'
    else:
        form = BehaviorForm()
        # This creates an empty form for when the user first opens up behavior_form.html

    context = {'form': form}
    return render(request, 'tracker/behavior/create_form.html', context)
    
def update_behavior(request, behavior_id):
    behavior = get_object_or_404(Behavior, id=behavior_id)
    
    if request.method == 'POST':
        form = BehaviorForm(request.POST, instance=behavior)

        if form.is_valid():
            form.save()
            redirect('tracker:home')
    else:
        form = BehaviorForm(instance=behavior)
    
    context = {
        'form': form,
        'behavior': behavior,
    }

    return render(request, 'tracker/behavior/update_form.html', context)