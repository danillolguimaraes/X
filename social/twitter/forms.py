from django import forms
from .models import Tweet

class TweetForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(attrs={
            "placeholder": "Digite seu Tweet aqui!",
            "class": "form-control",
        }),
        label="",  # Deixa o rótulo vazio
    )

    class Meta:
        model = Tweet
        exclude = ("user",)
