from django.contrib import admin

from .models import Target
from .forms import TargetForm


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ('url', 'created_at', 'handled_at',
                    'to_handle', 'timeshift')
    fieldsets = (
        ("Параметры",
            {'fields': ('url', )}),
        ('Процесс обработки',
            {'fields': ('created_at',
                        'handled_at',
                        'timeshift',
                        'to_handle',
                        'shed_at',
                        'task_id',)}),
        ('Данные',
            {'fields': ('title',
                        'heading',
                        'encoding')}))
    search_fields = ('id', 'url', 'title')
    readonly_fields = ('created_at', 'handled_at', 'shed_at', 'task_id')
    form = TargetForm
