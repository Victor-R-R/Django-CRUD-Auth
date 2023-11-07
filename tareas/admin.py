from django.contrib import admin
from .models import Tarea


class TareaAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


# Register your models here.
admin.site.register(Tarea, TareaAdmin)
