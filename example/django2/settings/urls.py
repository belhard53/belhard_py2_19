"""
URL configuration for setings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include, re_path

# from main import views


# все представления ниже берем тут
from app1.views  import hello3



urlpatterns = [
    # path('', index, name='index'),
    path('', include('main.urls')),
        
    # app1
    # дополнительные пути берем из приложения app1 - app1\urls.py
    # все они будут начинаться на http://127.0.0.1:7000/app1/
    path('app1/', include('app1.urls')),
    
    # при этом можем отсюда также прописать путь к любой вью-функции
    path('someurl/', hello3, name='otherhello3'),
    
    # админка - несколько путей могут вести к одному обработчику        
    path('admin/', admin.site.urls),
    path('adminka/', admin.site.urls),
    path('adminushka/', admin.site.urls),
       
]

