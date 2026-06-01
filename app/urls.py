from django.urls import path
from . import views

urlpatterns = [
    path('', views.survey_list, name='survey_list'),
    path('survey/<int:survey_id>/', views.survey_detail, name='survey_detail'),   
    path('survey/<int:survey_id>/vote/', views.vote, name='vote'), 
    path('survey/<int:survey_id>/results/', views.results, name='results'),
    path('profile/', views.profile_view , name='profile_view'),
    path('profile/edit/', views.MyProfile.as_view(), name='profile_edit'),
]
