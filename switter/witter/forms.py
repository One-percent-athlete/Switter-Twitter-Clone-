from django import forms
from .models import Swit

class SwitForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.widgets.Textarea(
        attrs={
        "placeholder": "What's In Your Mind?",
        "class": "form-control",
    }
    ),
    label="",
    )

    class Meta:
        model = Swit
        exclude = ["user"]