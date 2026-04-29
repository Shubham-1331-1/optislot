from django.urls import path
from . import views

urlpatterns = [
    path('', views.elective_list_view, name='elective_list'),
    path('choose/', views.submit_choices_view, name='submit_choices'),
]
