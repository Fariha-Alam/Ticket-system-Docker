from django.contrib import admin
from .models import ITChecklist

@admin.register(ITChecklist)
class ITChecklistAdmin(admin.ModelAdmin):
    list_display = ('task', 'is_active')
    list_editable = ('is_active',)
