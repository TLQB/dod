# Create your tests here.
from django.urls import path, include
from . import views


urlpatterns = [
    path('get-file-data/', views.get_file_data, name='get_file_data'),
    path("export_data_excel/", views.process_excel_data, name='export_data_excel'),
]