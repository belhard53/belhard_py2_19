import os
import django
import sys

from django.utils import timezone
from datetime import datetime, timedelta

# print(os.path.join(os.path.dirname(__file__), '..')) 
# print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setting.settings') 
django.setup()

from main.models import Course

def test_data():
    now = timezone.now()
    Course.objects.create(
                name="py", 
                course_num=97, 
                start_date=now.date(),  
                end_date=now + timedelta(days=15),  
                description='qqqqqq')

if __name__ == '__main__':
    test_data()
    
    
# ручной запуск    