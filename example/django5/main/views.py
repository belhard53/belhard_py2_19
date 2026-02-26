from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy, reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView


from .models import Student, Course, Grade
from .forms import CourseAddForm, CourseAddForm2, RegisterUserForm, StudentAddForm

from django.views.decorators.cache import cache_page



# для оптимизации запросов
# select_related	            prefetch_related
# -------------------------------------------------------
# Для ForeignKey и OneToOne	    Для ManyToMany и reverse ForeignKey
# JOIN в SQL	                Отдельные запросы + объединение в Python
# Один сложный запрос	        Несколько простых запросов


def index(r):
    return render(r, 'main/index.html')

# @cache_page(60*15)
def students(r):
    # взять всех студентов но при это связи на загрузятся
    # они будут грузиться автоматом при запросе для каждого студента отдельно
    # сколько студентов столько запросов
    students = Student.objects.all()
    
    # загрузить сразу отдельным запросом курсы из каждого студента
    # 2 запроса при любом количестве данных
    # students = Student.objects.prefetch_related('course').all()
    
    # или к примеру отдельным запросом по цепочке (двойное подчеркивание)
    # студенты -> у студентов оценки -> у оценок ее курс 
    # 3 запроса при любом количестве данных
    # students = Student.objects.prefetch_related('grades__course').all()
    # еще более сложная цепочка
    # students = Student.objects.prefetch_related('grades__course__student_set').all()
    
    # # все студенты со всеми курсами о оценками
    # for s in students:
    #     c = [f'{g.grade} - {g.course}' for g in s.grades.all()]        
    #     # print(type(c))
    #     print(s.name, ' - ' , c or 'нет оценок')
        
    # # если не обратится к данны students (например распечатать) запросов будет 0     
    # print('-----------------------')
    # print(f"Запросов: {len(connection.queries)}")
    # # print(students)
    # print('-----------------------')
    # print(f"Запросов: {len(connection.queries)}")
    
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
    

   
# добавить запись
class StudentAddView(LoginRequiredMixin, CreateView): # login дб первый
# class StudentAddView(CreateView): 
    form_class = StudentAddForm
    template_name = 'main/student_add_form.html'
    # template_name = 'student_add_form_manual.html' # тут форма создается вручную
    success_url = reverse_lazy('students')
    login_url = '/login/'



# изменить данные
class StudentEditView(UpdateView):
    model = Student
    fields = '__all__'
    template_name = 'main/student_edit_form.html'
    pk_url_kwarg = 'id'
    # Если form_class не указан, автоматически создаёт форму на основе  модели
    


# # изменить данные - через функцию
@login_required(login_url='/login/')
def student_edit_view(r, id):    
    student = get_object_or_404(Student, id=id)    
    if r.method=='GET':        
        return render(
                    request=r, 
                    template_name='main/student_edit_form.html', 
                    context={'form':StudentAddForm(instance=student), 'id':id})
    # POST
    form = StudentAddForm(r.POST, instance=student)
    if form.is_valid(): 
        print(form.cleaned_data)
        form.save()
        return redirect('students')   
    form.add_error(None, "Ошибка....")
    return render(r, 'student_edit_form.html', {'form':form})     

    
    
# ----------------------- COURSES
class Courses(ListView):
    model = Course
    template_name = 'main/courses.html'
    context_object_name = 'courses' 

class Show_course(DetailView):
    model = Course
    template_name = 'main/course.html'
    pk_url_kwarg = 'id'        
    

# используя ручную форму    
def course_add_view(r):
    if r.method == "POST":
        form = CourseAddForm(r.POST)        
        if form.is_valid():        
            try:                
                Course.objects.create(**form.cleaned_data)
                return redirect("courses")
            except Exception as e:
                form.add_error(None, "Ошибка ....")
                print(e)
    else:
        form = CourseAddForm()
    return render(r, 'main/course_add_form.html', context={'form':form})



@login_required(login_url='/login/')
def course_add_view2(r):
    if r.method == "POST":
        form = CourseAddForm2(r.POST)        
        if form.is_valid():
            form.save()
            return redirect("courses")    
    else:
        form = CourseAddForm2()
    return render(r, 'main/course_add_form.html', context={'form':form})    


class CourseEditView(UpdateView):
    model = Course
    fields = '__all__'    
    template_name = 'main/course_add_form.html'
    pk_url_kwarg = 'id'
    
    # если не указать success_url будет переходить на страницу этого курса через Course.get_absolute_url()
    # success_url = reverse_lazy('courses')
   
class CourseDeleteView(DeleteView):
    model = Course      
    template_name = 'main/course_del_confirm.html'    
    success_url = reverse_lazy('courses')
    
    




# -----------------------------------

class LoginUser(LoginView):
    form_class = AuthenticationForm 
    template_name = 'main/login.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('index')

class RegisterUser(CreateView):
    # form_class = UserCreationForm # джанговская формма
    form_class = RegisterUserForm # своя форма на основе джанговой
    template_name = 'main/reg.html'
    success_url = reverse_lazy('login') # для входа сайта
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')
    
    
def logout_user(r):
    logout(r)
    return redirect('index')        