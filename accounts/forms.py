from django import forms
from .models import Account


class Signupform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control floating'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control floating'}))

    class Meta:
        model = Account
        fields = ['name', 'phone_number', 'email', 'password']



    def __init__(self, *args, **kwargs):
        super(Signupform, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control floating'
