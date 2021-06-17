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

    def clean(self):
        data = super(Signupform, self).clean()
        print(data)
        password = data['password']
        confirm_password = data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError('Passwords should match!')

    def __init__(self, *args, **kwargs):
        super(Signupform, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control floating'
