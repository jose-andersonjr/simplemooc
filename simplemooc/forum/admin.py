from django.contrib import admin

from .models import Thread, Reply


class ThreadAdmin(admin.ModelAdmin):

    list_display = ['titulo', 'autor', 'created', 'modified']
    search_fields = ['titulo', 'author__email', 'corpo']


class ReplyAdmin(admin.ModelAdmin):

    list_display = ['thread', 'autor', 'created', 'modified']
    search_fields = ['thread__titulo', 'autor__email', 'reply']


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Reply, ReplyAdmin)