from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(
        label='Search for',
        max_length=100,
        widget=forms.TextInput(attrs={'class': ''})
    )
