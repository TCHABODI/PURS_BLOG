from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.conf import settings

from . import forms
from django.shortcuts import redirect, render

# Create your views here.

# def logout_user(request):
#     logout(request)
#     return redirect('login')
from .models import User


class LoginPageView(View):
    form_class = forms.LoginForm
    template_name = 'authentication/login.html'

    def get(self, request):
        form = self.form_class()
        message = ''

        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            message = 'Identifiants invalides.'
        return render(request, self.template_name, context={'form': form, 'message': message})

@login_required
def upload_profile_photo(request):
    form = forms.UploadProfilePhotoForm(instance=request.user)
    if request.method == 'POST':
        form = forms.UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # now we can save
            form.save()
            return redirect('home')
    return render(request, 'authentication/change_profile.html', context={'form': form})

def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})
