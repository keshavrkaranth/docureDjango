from django.core.exceptions import ValidationError
from django.shortcuts import render
from .forms import Signupform
from .models import Account

# Create your views here.


def signup(request):
    form = Signupform()
    if request.method == 'POST':
        form = Signupform(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            print(name)
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            username = email.split('@')[0]
            user = Account.objects.create_user(
                name=name, username=username, email=email, password=password)
            user.phone_number = phone_number
            user.is_active = True
            user.save()
        else:
            form = Signupform()

    data = {
        'form': Signupform()
    }
    return render(request, 'accounts/signup.html', data)
