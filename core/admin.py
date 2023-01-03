from django.contrib import admin
from .models import Tontine

# Register your models here.

# Admin Models
# @admin.register(Tontine)
class TontineAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'creation_date', 'number_of_members']
    search_fields = ['name', 'creation_date']
    list_filter = ['name', 'creation_date']
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

# Register models in admin panel
admin.site.register(Tontine, TontineAdmin)
