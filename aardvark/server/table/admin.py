from django.contrib import admin
from .models import Table, TableAdmin

admin.site.register(Table, TableAdmin)
