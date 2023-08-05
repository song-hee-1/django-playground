
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from accounts.forms import UserForm


# Create your views here.
def signup(request):
    """
    회원가입
    """
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('raw_password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
        return render(request, 'accounts/signup.html', {'form':form})