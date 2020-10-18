from django.contrib import admin

from .models import Resident,Invoice,Receipt

admin.site.register(Resident)
admin.site.register(Receipt)
admin.site.register(Invoice)