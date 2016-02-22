from django.contrib import admin
from menu.models import Menu, MenuAdmin

# Register your models here.
admin.site.register(Menu, MenuAdmin)