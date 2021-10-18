from django.contrib import admin
from app.models import Todo

# Register your models here.
class TodoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Todo, TodoAdmin)