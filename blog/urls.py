from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('category/<slug:slug>/', views.category_detail, name='category'),
    path('tag/<slug:slug>/', views.tag_detail, name='tag'),
    path('<slug:slug>/', views.post_detail, name='detail'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]