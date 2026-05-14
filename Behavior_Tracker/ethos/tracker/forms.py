from django import forms
from .models import Behavior

class BehaviorForm(forms.ModelForm):
    class Meta:
        model = Behavior
        fields = ['title', 'description']

    """
    What this does is it takes all the fields from the Behavior model
    that are defined within the attribute "fields = [...]" of the Meta class and uses the 
    formfield() method to create the HTML input fields that correspond to the
    field types that I defined within the Behavior mdoel. Ex. models.CharField
    will result to a small text box while models.TextField will result to a big multiline
    text box.
    """