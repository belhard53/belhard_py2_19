from django.shortcuts import render
from .models import Student

# Create your views here.

def index(r):
    return render(r, 'main/index.html')


def students(r):
    students = Student.objects.all()
    return render(r, 'main/students.html', 
                    context={'students':students})