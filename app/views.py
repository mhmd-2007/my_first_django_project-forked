from django.shortcuts import render, get_object_or_404
from .models import Survey, Choice
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

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

def vote(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id, is_active=True)

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

        return HttpResponseRedirect(reverse('results', args=(survey.id,)))
    
def result(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id, is_active=True)

    total_votes = sum(choice.votes for choice in survey.choice_st.all())

    choices_with_perchetage = []
    for choice in survey.choice_set.all():
        if total_votes > 0:
            percentage = (choice.votes / total_votes) * 100
        else:
            percentage = 0
        choices_with_perchetage.append({
            "choice" : choice,
            "percentage" : round(percentage, 2),
        })
        
    return render(request, "app/result.html", {
        "survry" : survey,
        "choices_with_percentage" : choices_with_perchetage, 
        "total_votes" : total_votes,
    })