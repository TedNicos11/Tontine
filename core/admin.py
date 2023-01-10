from django.contrib import admin
from .models import Tontine

# Register your models here.

# Admin Models
class TontineAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'creation_date', 'number_of_members']
    search_fields = ['name', 'creation_date']
    list_filter = ['name', 'creation_date']

# Register models in admin panel
admin.site.register(Tontine, TontineAdmin)
