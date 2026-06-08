from .models import Survey, Choice, Vote
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.db import models
from django.core.paginator import Paginator
from django.db.models import Sum

def survey_list(request):
    search_query = request.GET.get('q', '')
    surveys = Survey.objects.filter(is_active=True)
    sort_by = request.GET.get('sort', '-created_at')
    
    if search_query:
        surveys = surveys.filter(
            models.Q(question__icontains=search_query) | 
            models.Q(product__name__icontains=search_query)    
        )
    
    if sort_by == "-total_votes":
        surveys = surveys.annotate(
            total_votes = Sum('choice__votes')
        ).order_by("-total_votes")
    else :                 
        surveys = surveys.order_by(sort_by)

    paginator = Paginator(surveys, 6)
    page_number = request.GET.get("page")
    if not page_number:
        page_number = 1
    page_obj = paginator.get_page(page_number) 

    return render(request, "app/survey_list.html", {
        'surveys' : page_obj,
        "search_query" : search_query,
        "current_sort" : sort_by,
    })

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

