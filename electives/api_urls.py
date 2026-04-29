from django.urls import path
from .api_views import ElectiveListAPI, ChoiceListAPI

urlpatterns = [
    path('electives/', ElectiveListAPI.as_view(), name='api_electives'),
    path('choices/', ChoiceListAPI.as_view(), name='api_choices'),
]
