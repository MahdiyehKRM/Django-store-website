from django import forms


class VariantForm(forms.Form):
    select = forms.CharField()


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50)
