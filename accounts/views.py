from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, aauthenticate
from django.contrib.auth.forms import AuthenticationForm 
from .forms import RegisterForm
from accounts.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('survey_list')
    else: 
        form = RegisterForm()

    return render(request, 'accounts/register.html', {
        'form' : form
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('survey_list')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form' : form})

def logout_view(request):
    logout(request)
    return redirect('survey_list')

class MyProfile(LoginRequiredMixin, View):
    def get(self, request):
        '''display profile forms with current informations'''
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'user_form' : user_form,
            'profile_form' : profile_form, 
            'title' : 'ویرایش پروفایل'
        }
        return render(request, 'accounts/profile_edit.html', context)
    
    def post(self, request):
        user_form = UserUpdateForm(
            request.POST,
            instance = request.user
        )
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance = request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Your profile has been updated successfully')
            return redirect('profile_view')#redirect to display profile page
        
        else: 
            messages.error(request, 'خطا در به روزرسانی پروفایل. لطفا اطلاعات رو بررسی کنید.')
            context = {
                'user_form' : user_form,
                'user_profile' : profile_form,
                'title' : 'editing the profile'
            }

            return render(request, 'accounts/profile_edit.html', context)

@login_required        
def profile_view(request):
    '''
    simple showing of users informations(without edit form)
    this view is used for display users informations
    '''
    user = request.user
    profile = user.profile

    return render(request, 'accounts/profile_display.html', {
        "user" : user,
        'profile' : profile,
    })