from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('tasks/new', views.TaskCreateView.as_view(), name='task-new'),
    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('category/new', views.CategoryCreateView.as_view(), name='category-new'),
]