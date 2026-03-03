from django.apps import AppConfig



class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    verbose_name = "Академия Ы"
    




# создание сигнала который запускает скрипт после каждой миграции
    # def ready(self):
    #     # Подключаем сигнал только для этого приложения
    #     if settings.DEBUG or settings.TESTING:
    #         post_migrate.connect(create_test_data, sender=self)


# def create_test_data(sender, **kwargs):
#     # Импортируем модели внутри функции, чтобы избежать проблем с загрузкой приложений
#     from django.contrib.auth.models import User
#     from .models import Course

#     # Проверяем, не существуют ли уже тестовые данные
#     if Course.objects.count() == 0:
#         # Создаем тестовые данные
#         Course.objects.create(name="Тестовый курс")
#         print("Тестовые данные созданы")


#     # Создание тестового пользователя
#     if not User.objects.filter(username='testuser').exists():
#         User.objects.create_user(
#             username='testuser',
#             email='test@example.com',
#             password='testpass123',
#             first_name='Тестов',
#             last_name='Пользователь'
#         )
#         print("Создан тестовый пользователь: testuser / testpass123")
    
#     # Создание суперпользователя если его нет (только в разработке)
#     if settings.DEBUG and not User.objects.filter(is_superuser=True).exists():
#         User.objects.create_superuser(
#             username='admin',
#             email='admin@example.com', 
#             password='1234'
#         )
#         print("Создан суперпользователь: admin / 1234")
    
#     print("---------------- Тестовые данные успешно созданы! -------------------")


