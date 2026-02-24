# models.py — ВСЕ типы полей Django 6.0 с описаниями!

from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid

class UniversalModel(models.Model):
    # 🔢 ID [AutoField/BigAutoField/SmallAutoField]
    id = models.BigAutoField(primary_key=True)  # Автоинкремент PK
    
    # 📝 Текст [CharField/TextField/SlugField/EmailField/URLField]
    char = models.Cd(max_length=100, default="text")           # Строка до 100 символов
    text = models.TextFharFielield(blank=True)                               # Длинный текст (неограниченно)
    slug = models.SlugField(unique=True)                              # a-z0-9- (URL friendly)
    email = models.EmailField()                                       # Валидация email
    url = models.URLField()                                           # Валидация URL
    
    # 🔢 Числа [Integer/BigInteger/SmallInteger/Positive/Decimal/Float]
    integer = models.IntegerField()                                   # -2³¹..2³¹-1
    big_int = models.BigIntegerField()                                # -2⁶³..2⁶³-1
    small_int = models.SmallIntegerField()                            # -32k..32k
    positive_int = models.PositiveIntegerField()                      # 0..2³¹-1
    positive_small_int = models.PositiveSmallIntegerField()           # 0..32k
    decimal = models.DecimalField(max_digits=10, decimal_places=2)    # 99999999.99 (точность!)
    float_f = models.FloatField()                                     # Плавающая точка
    
    # ✅ Логические [BooleanField/NullBooleanField]
    boolean = models.BooleanField(default=False)                      # True/False чекбокс
    null_boolean = models.BooleanField(null=True, blank=True)         # True/False/NULL
    
    # 📅 Время [DateField/DateTimeField/TimeField/DurationField]
    date = models.DateField()                                         # 2026-02-20
    time = models.TimeField()                                         # 14:30:25
    datetime = models.DateTimeField(auto_now_add=True)                # 2026-02-20 14:30:25
    duration = models.DurationField()                                 # timedelta (1 день 2 часа)
    
    # 🗂️ Файлы [FileField/ImageField]
    file_f = models.FileField(upload_to='files/')                     # Загрузка файлов
    image = models.ImageField(upload_to='images/')                    # Изображения (Pillow)
    
    # 🌐 Сеть [GenericIPAddressField/UUIDField]
    ip = models.GenericIPAddressField()                               # IPv4/IPv6
    uuid_f = models.UUIDField(default=uuid.uuid4, editable=False)     # 550e8400-e29b-41d4-a716-446655440000
    
    # 🔗 Связи [ForeignKey/OneToOneField/ManyToManyField]
    fk = models.ForeignKey('self', on_delete=models.CASCADE)          # Один-ко-многим
    o2o = models.OneToOneField('self', on_delete=models.CASCADE)      # Один-к-одному
    m2m = models.ManyToManyField('self', related_name='m2m')          # Многие-ко-многим
    
    # 🎨 Выбор [CharField(choices=)]
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
        ('archived', 'Архив'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    # 📊 PostgreSQL [ArrayField/JSONField]
    array_int = ArrayField(models.IntegerField())                     # [1,2,3] PostgreSQL only
    array_char = ArrayField(models.CharField(max_length=10))          # ['a','b','c']
    json = models.JSONField(default=dict)                             # {"key": "value"}
    
    # 🔢 Бинарник
    binary = models.BinaryField()                                     # bytes/raw данные
    
    class Meta:
        db_table = 'universal_model'
        
    def __str__(self):
        return f"Universal #{self.id}"
