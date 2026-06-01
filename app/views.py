from .models import Survey, Choice, Vote, Profile
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm

def survey_list(request):
    surveys = Survey.objects.filter(is_active=True)
    return render(request, "app/survey_list.html", {"surveys": surveys})

def survey_detail(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id, is_active=True)
    choices = survey.choice_set.all()
    return render(request, "app/survey_detail.html", {
        'survey': survey,
        'choices': choices,
    })

@login_required
def vote(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id, is_active=True)

    existing_vote = Vote.objects.filter(user=request.user, choice__survey=survey).first()
    if existing_vote:
        choices = survey.choice_set.all()
        return render(request, 'app/survey_detail.html', {
            'survey' : survey,
            'choices' : choices, 
            'error_message' : "شما قبلا به این نظرسنجی رای داده اید.",
        })

    try:
        selected_choice = survey.choice_set.get(pk=request.POST['choice'])
    except:
        choices = survey.choice_set.all()
        return render(request, 'app/survey_detail.html', {
            'survey' : survey,
            'choices' : choices,
            'error_message' : "لطفا یکی از گزینه های زیر را انتخاب کنی.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        Vote.objects.create(user=request.user, choice=selected_choice)

        return HttpResponseRedirect(reverse('results', args=(survey.id,)))

def results(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id, is_active=True)

    total_votes = sum(choice.votes for choice in survey.choice_set.all())

    choices_with_percentage = []
    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = Vote.objects.get(user=request.user, choice__survey=survey)
        except Vote.DoesNotExist:
            user_vote = None

    for choice in survey.choice_set.all():
        if total_votes > 0:
            percentage = (choice.votes / total_votes) * 100
        else:
            percentage = 0
        choices_with_percentage.append({
            "choice" : choice,
            "percentage" : round(percentage, 2),
            "is_user_vote" : user_vote and user_vote.choice.id == choice.id,
        })
        
    return render(request, "app/results.html", {
        "survey" : survey,
        "choices_with_percentage" : choices_with_percentage, 
        "total_votes" : total_votes,
        "user_vote" : user_vote,
    })

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
        return render(request, 'app/profile_edit.html', context)
    
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

            return render(request, 'app/profile_edit.html', context)

@login_required        
def profile_view(request):
    '''
    simple showing of users informations(without edit form)
    this view is used for display users informations
    '''
    user = request.user
    profile = user.profile

    return render(request, 'app/profile_display.html', {
        "user" : user,
        'profile' : profile,
    })
