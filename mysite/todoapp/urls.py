from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('tasks/new', views.TaskCreateView.as_view(), name='task-new'),
    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('tasks/<int:pk>', views.TaskDetailView.as_view(), name='task'),
    path('tasks/<int:pk>/steps', views.StepListView.as_view(), name='steps'),
    path('tasks/<int:pk>/step', views.StepCreateView.as_view(), name='step'),
    path('step/<int:pk>/delete', views.StepDeleteView.as_view(), name='step-delete'),
    path('step/<int:pk>/update', views.StepUpdateView.as_view(), name='step-update'),
    path('tasks/<int:pk>/update', views.TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete', views.TaskDeleteView.as_view(), name='task-delete'),
    path('category/new', views.CategoryCreateView.as_view(), name='category-new'),
    path('category/<int:pk>/delete', views.CategoryDeleteView.as_view(), name='category-delete'),
    path('category/<int:pk>/update', views.CategoryUpdateView.as_view(), name='category-update'),

]