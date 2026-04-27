from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from .forms import SignUpForm, LoginForm

class CustomLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('products:product_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
