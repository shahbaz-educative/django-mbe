from django.contrib import admin
from sample_app.models import *

# Register your models here.
admin.site.register(Author)
admin.site.register(Question)
admin.site.register(Choice)