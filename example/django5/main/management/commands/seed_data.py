from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Course

from django.utils import timezone
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Заполняет базу тестовыми данными'

    def handle(self, *args, **options):
        # Очистка старых данных (опционально)        
        # Course.objects.all().delete()
        
        
        now = timezone.now()
        
        # Создание категорий
        c = Course.objects.create(name="py", 
                                course_num=101, 
                                start_date=now.date(),  # Только дата
                                end_date=now + timedelta(days=15),  # Дата и время)
                                description='qqqqqq'
        )
        
        # start_time=datetime.strptime("14:00", "%H:%M").time()
        
        # Создание тестового пользователя
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='1234'
            )
        
        self.stdout.write(
            self.style.SUCCESS('Тестовые данные успешно созданы!!')
        )