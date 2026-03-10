from django.urls import path
from .views import run_add_task, tasks_overview

urlpatterns = [
    path('', tasks_overview, name='tasks_overview'),
    path('run-add/', run_add_task, name='run_add_task'),
]
