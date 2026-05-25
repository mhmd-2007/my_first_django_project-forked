from django.urls import path
from . import views

urlpatterns = [
    path('', views.survey_list, name='survey_list'),
    path('survey/<int:survay_id>/', views.survey_detail, name='survey_detail'),   
    path('survey/<int:survey_id>/vote', views.vote, name='vote'), 
]
