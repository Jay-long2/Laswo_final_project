from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='list'),
    path('category/<slug:slug>/', views.project_category, name='category'),
    path('<slug:slug>/', views.project_detail, name='detail'),
]