from django.contrib import admin

from .models import Student, Course, Grade

# admin.site.register(Student) 

admin.site.register(Course)



class GradeInline(admin.TabularInline):
    model = Grade
    extra = 1
    fields = ('course', 'grade', 'date')
    ordering = ('-date',)
    # autocomplete_fields = ('course',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'sex', 'short_name', 'average_grade', 'average_grade2')
    # list_display_links = ('surname', 'name')
    # list_editable = ('surname', 'name')
    search_fields = ('name', 'surname')
    list_filter = ('sex', 'active')
    inlines = [GradeInline]
    filter_horizontal = ('course',) # при добавление перекидывать с поля в поле
    # filter_vertical = ('course',) # при добавление перекидывать с поля в поле
    
    def average_grade(self, obj):        
        gs = [g.grade for g in obj.grades.all()]
        return round(sum(gs)/len(gs),2) if gs else '---'
    
    def average_grade2(self, obj):
        from django.db.models import Avg
        res = Grade.objects.filter(person=obj).aggregate(Avg('grade', default=0))
        return res['grade__avg']
    
    
    def short_name(self, obj):
        return f"{obj.surname} {obj.name[0]}."
    
    short_name.short_description = "Короткое имя"


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('person', 'course', 'grade', 'date', 'date_add', 'date_update')
    list_filter = ('course', 'grade', 'date')
    search_fields = ('person__surname', 'person__name')
    # autocomplete_fields = ('person', 'course') # при выборе список с фильтром и ajax догружает
    autocomplete_fields = ('person',) # при выборе список с фильтром и ajax догружает
    date_hierarchy = 'date' # создает иерархию дат
    ordering = ('-date',)