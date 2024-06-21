from django.contrib import admin
from .models import Club, Game


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_by')
    search_fields = ('name', 'created_by')
    filter_horizontal = ('members', 'games')
