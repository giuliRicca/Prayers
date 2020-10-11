from django import forms
from .models import Prayer


class PrayerForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Título'}))
    body = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Cuerpo'}))
    private = forms.ComboField
    category = forms.ChoiceField(choices=Prayer.PRAYER_CATEGORIES)

    class Meta:
        model = Prayer
        fields = ['title', 'body', 'category', 'private']
