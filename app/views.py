from django.shortcuts import render
from .models import Survey

# Create your views here.

def survey_list(request):
    surveys = Survey.objects.filter(is_active=True)
    return render(request, "app/survey_list.html", {"surveys": surveys})
