from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('run/', views.run_allotment_view, name='run_allotment'),
    path('revert/', views.revert_allotment_view, name='revert_allotment'),
    path('export-csv/', views.export_csv_view, name='export_csv'),
]
