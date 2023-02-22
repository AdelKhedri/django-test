from django import forms

class SearchForms(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    content = forms.CharField(max_length=500, required=False)
    publish_time_hieght = forms.DateTimeField( required=False)
    publish_time_low = forms.DateTimeField(required=False)
    active = forms.BooleanField(required=False)
    is_delete = forms.BooleanField(required=False)
    author = forms.CharField(max_length=200, required=False)
    views = forms.CharField(max_length=300, required=False)
    likes = forms.CharField(max_length=300, required=False)