from django import forms
from .models import Action

class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ['status', 'recorded_by']