from django import forms


class IndexForm(forms.Form):
    room_name = forms.CharField(max_length=100)

