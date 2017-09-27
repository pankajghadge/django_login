from django import forms

from desiquotes.quotes.models import Quote


class QuoteForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=4000)

    class Meta:
        model = Quote
        fields = ['content', 'tags', 'status']
