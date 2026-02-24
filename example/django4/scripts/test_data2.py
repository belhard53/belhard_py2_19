import os
import django


from django.utils import timezone
from datetime import datetime, timedelta
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setting.settings') 
django.setup()

from main.models import Course

def seed_database():
    now = timezone.now()
    Course.objects.create(
                name="py", 
                course_num=98, 
                start_date=now.date(),  # Только дата
                end_date=now + timedelta(days=15),  # Дата и время)
                description='qqqqqq')

if __name__ == '__main__':
    seed_database()
    
    

# linux ./manage.py shell < scripts/myscript.py