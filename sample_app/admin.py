from django.contrib import admin
from sample_app.models import *

# admin.site.empty_value_display = '(No value)'

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    
    empty_value_display = 'Unknown'
    list_display = ('name','createdDate','updatedDate',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    save_on_top = True

    fieldsets = (
        ("Question information", {'fields': ('question_text',)}),
        ("Date", {'fields': ('pub_date',)}),
        ('The author', {'classes': ('collapse',),'fields': ('refAuthor',),}),
    )

    list_display = ('question_text', 'refAuthor','pub_date','createdDate', 'updatedDate',)
    list_display_links = ('refAuthor',)
    list_editable = ('question_text',)

    ordering = ('-pub_date', 'createdDate',)

    date_hierarchy = 'pub_date'


admin.site.register(Choice)
