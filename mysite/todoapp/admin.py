from django.contrib import admin
from .models import Task, Step, Category, Profile

admin.site.register(Task)
admin.site.register(Step)
admin.site.register(Category)
admin.site.register(Profile)

