from django.urls import path
from .api_views import AllotmentResultsAPI, RunAllotmentAPI

urlpatterns = [
    path('allotment/run/', RunAllotmentAPI.as_view(), name='api_run_allotment'),
    path('allotment/results/', AllotmentResultsAPI.as_view(), name='api_allotment_results'),
]
