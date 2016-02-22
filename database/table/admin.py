from django.contrib import admin
from table.models import Table, TableAdmin

# Register your models here.
admin.site.register(Table, TableAdmin)