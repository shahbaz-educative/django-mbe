from django.contrib import admin
from sample_app.models import *


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','createdDate','updatedDate',)

admin.site.register(Question)
admin.site.register(Choice)
