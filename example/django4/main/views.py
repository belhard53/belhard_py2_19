from django.shortcuts import render
from .models import Student, Course, Grade
from django.db import connection

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.db.models import Q
# Create your views here.


# для оптимизации запросов
# select_related	            prefetch_related
# -------------------------------------------------------
# Для ForeignKey и OneToOne	    Для ManyToMany и reverse ForeignKey
# JOIN в SQL	                Отдельные запросы + объединение в Python
# Один сложный запрос	        Несколько простых запросов


def index(r):
    return render(r, 'main/index.html')


def students(r):
    # взять всех студентов но при это связи на загрузятся
    # они будут грузиться автоматом при запросе для каждого студента отдельно
    # сколько студентов столько запросов
    # students = Student.objects.all()
    
    # загрузить сразу отдельным запросом курсы из каждого студента
    # 2 запроса при любом количестве данных
    # students = Student.objects.prefetch_related('course').all()
    
    # или к примеру отдельным запросом по цепочке (двойное подчеркивание)
    # студенты -> у студентов оценки -> у оценок ее курс 
    # 3 запроса при любом количестве данных
    students = Student.objects.prefetch_related('grades__course').all()
    # еще более сложная цепочка
    # students = Student.objects.prefetch_related('grades__course__student_set').all()
    
    # # все студенты со всеми курсами о оценками
    for s in students:
        c = [f'{g.grade} - {g.course}' for g in s.grades.all()]        
        # print(type(c))
        print(s.name, ' - ' , c or 'нет оценок')
        
    # если не обратится к данны students (например распечатать) запросов будет 0     
    print('-----------------------')
    print(f"Запросов: {len(connection.queries)}")
    # print(students)
    print('-----------------------')
    print(f"Запросов: {len(connection.queries)}")
    
    # for query in connection.queries:
    #     print('-----sql-------')
    #     print(query['sql'])    
    
    return render(r, 'main/students.html', 
                    context={'students':students})
    
def student(r, id):
    student = Student.objects.get(id=id)    
    return render(r, 'main/student.html', context={'student':student})        


class StudentsView(ListView):
    model = Student
    template_name = 'main/students.html'
    context_object_name = 'students'
    paginate_by = 10
    paginate_orphans = 3  # Не создавать страницу с <3 объектами
    
    
    
    # можно добавить необязательные параметры
    
    # для уточнения запроса если нет "def get:"
    def get_queryset(self):
        # queryset  = Student.objects.filter(name='Вася')
        queryset  = super().get_queryset() # взять все или Student.objects.all()
        # http://127.0.0.1:8000/students2/?q=оро
        query = self.request.GET.get('q', '').strip()
        
        if query:
            import re
            
            
            # name__icontains в sqlite не работает с кириллицей поэтому - name__iregex
            queryset = queryset.filter(
                (Q(name__iregex=query) | Q(surname__iregex=query)) &
                ~Q(age__gt=60) # не больше 60
            )            
            
            # Оператор ~ (NOT — отрицание)
            # Оператор & (AND — И)
            # Оператор | (OR — ИЛИ)
            
        return queryset
    
    # для добавления в контекст доп данных если нет "def get"
    # def get_context_data(self, **kwargs) -> dict[str, Any]:
    #     context =  super().get_context_data(**kwargs)
    #     context['menu'] = menu
    #     return context
    
    # можно переписать метод обслуживающий get-запрос для 
    # считывания доп параметров
    # http://127.0.0.1:8000/students2/?q=ас
    # def get(self, r, *args, **kwargs):
    #     q = r.GET.get('q', default='')
    #     # print(f)
    #     # к примеру фильтр на содержание в имени подстроки из параметров в get
    #     # можно на странице сделать поле для фильтра
    #     students = Student.objects.filter(name__contains=q).all()
    #     return render(r, self.template_name, context={'students':students})
    
    
  
# просмотр одной записи    
class StudentView(DetailView):
    model = Student
    template_name = 'main/student.html'              
    context_object_name = 'student'    
    pk_url_kwarg = 'pk' # т.к. тут slug ссылка по id уже не нужна
    # slug_url_kwarg = 'name_slug'
    # login_url = '/login/'          
    
    
    
# ----------------------- COURSES
class Courses(ListView):
    model = Course
    template_name = 'main/courses.html'
    context_object_name = 'courses' 

class Show_course(DetailView):
    model = Course
    template_name = 'main/course.html'
    pk_url_kwarg = 'id'        