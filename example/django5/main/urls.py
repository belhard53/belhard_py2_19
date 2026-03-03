
from django.urls import path, include

from .views  import *

urlpatterns = [     
               
    path('', index, name='index'),
    
    path('students/', students, name='students'),
    path('students2/', StudentsView.as_view(), name='students2'),
    
    
    path('students/<int:id>/', student, name='student'),
    # path('students2/<int:pk>/', StudentView.as_view(), name='student2'),
    path('students2/<slug:name_slug>/', StudentView.as_view(), name='student2'),
    
    path('students/add/', StudentAddView.as_view(), name='student_add'),        
    path('students/<int:id>/edit/', StudentEditView.as_view(), name='student_edit'),      
    # # то же - через функцию
    path('students/<int:id>/edit2/', student_edit_view, name='student_edit2'),
    
    # если нужен кеш - включается или тут или на views декоратором
    # path('courses/', cache_page(60*15)(Courses.as_view()), name='courses',),
    
    path('courses/', Courses.as_view(), name='courses',),    
    path('courses/<int:id>/', Show_course.as_view(), name='course',),
    # path('courses/add/', course_add_view, name='course_add',),    
    path('courses/add/', course_add_view2, name='course_add',),    
    path('courses/<int:id>/edit/', CourseEditView.as_view(), name='course_edit',),
    path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete',),
    
    
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('reg/', RegisterUser.as_view(), name='reg'),
    
    
]