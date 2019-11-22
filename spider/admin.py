from django.contrib import admin

# Register your models here.
from .models import Reference


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('url_id', 'crawled_uri', 'created_at')
admin.site.register(Reference, ReferenceAdmin)
