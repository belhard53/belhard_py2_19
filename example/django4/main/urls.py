
from django.urls import path, include

from .views  import *

urlpatterns = [     
               
    path('', index, name='index'),
    
    path('students/', students, name='students'),
    path('students2/', StudentsView.as_view(), name='students2'),
    
    path('students/<int:id>/', student, name='student'),
    path('students2/<int:pk>/', StudentView.as_view(), name='student2'),
    
    path('courses/', Courses.as_view(), name='courses',),    
    path('courses/<int:id>/', Show_course.as_view(), name='course',),
    
    
    
]