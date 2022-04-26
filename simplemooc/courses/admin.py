from sys import displayhook
from django.contrib import admin
from .models import Course, Enrollment, Announcement, Comment, Aula, Materiais

class CourseAdmin(admin.ModelAdmin): #classe que representa as opçoes do curso
    list_display = ['name', 'slug', 'start_date', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}

class MaterialInlineAdmin(admin.TabularInline):
    model  = Materiais


class AulaAdmin(admin.ModelAdmin):
    
    list_display = ['nome', 'numero', 'curso', 'release_date']
    campo_busca = ['nome', 'descricao']
    list_filter = ['created_at']
    inlines = [
        MaterialInlineAdmin
        ]
    
    

admin.site.register(Course, CourseAdmin)
admin.site.register([Enrollment, Announcement, Comment, Materiais])
admin.site.register(Aula, AulaAdmin)