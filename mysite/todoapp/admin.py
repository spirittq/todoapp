from django.contrib import admin
from .models import Task, Step, Category, Profile


class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'category', 'date_created', 'due, date', 'status', 'importnace')

admin.site.register(Task, TaskAdmin)
admin.site.register(Step)
admin.site.register(Category)
admin.site.register(Profile)

