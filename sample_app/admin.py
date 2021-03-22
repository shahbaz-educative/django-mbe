from django.contrib import admin
from sample_app.models import *
import csv
from datetime import datetime, timedelta
from django.utils.html import format_html
from django.http import HttpResponse

# admin.site.empty_value_display = '(No value)'

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    empty_value_display = 'Unknown'
    list_display = ('name','createdDate','updatedDate',)
    search_fields = ('name',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    save_on_top = True

    fieldsets = (
        ("Question information", {'fields': ('question_text',)}),
        ("Date", {'fields': ('pub_date',)}),
        ('The author', {'classes': ('collapse',),'fields': ('refAuthor',),}),
    )

    list_display = ('question_text', 'colored_question_text', 'goToChoices', 'refAuthor', 'has_been_published', 'pub_date', 
                    'createdDate', 'updatedDate',)

    list_display_links = ('refAuthor',)
    list_editable = ('question_text',)

    def has_been_published(self, obj):
        present = datetime.now()
        return obj.pub_date.date() < present.date()

    def colored_question_text(self, obj):
	    return format_html('<span style="color: #{};">{}</span>', "ff5733", obj.question_text,)


    has_been_published.short_description = 'Published?'
    has_been_published.boolean = True

    def make_published(modeladmin, request, queryset):
        queryset.update(pub_date=datetime.now()- timedelta(days=1))

    make_published.short_description = "Mark selected questions as published"

    def export_to_csv(modeladmin, request, queryset):
        opts = modeladmin.model._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; \filename={}.csv'.format(opts.verbose_name)
        writer = csv.writer(response)
        fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
        
        # Write a first row with header information
        writer.writerow([field.verbose_name for field in fields])
    
        # Write data rows
        for obj in queryset:
            data_row = []
            for field in fields:
                value = getattr(obj, field.name)
                if isinstance(value, datetime):
                    value = value.strftime('%d/%m/%Y %H:%M')
                data_row.append(value)
            writer.writerow(data_row)
    
        return response
    
    export_to_csv.short_description = 'Export to CSV'

    actions = [make_published, export_to_csv]

    # @mark_safe
    def goToChoices(self, obj):
	    return format_html('<a class="button" href="/admin/sample_app/choice/?question__id__exact=%s" target="blank">Choices</a>&nbsp;'% obj.pk)
    
    goToChoices.short_description = 'Choices'
    goToChoices.allow_tags = True

    # ordering = ('-pub_date', 'createdDate',)
    # date_hierarchy = 'pub_date'
    # list_filter = ('refAuthor',)
    list_select_related = ('refAuthor',)
    # autocomplete_fields = ['refAuthor']
    raw_id_fields = ('refAuthor', )


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice_text','votes','createdDate', 'updatedDate',)
    list_filter = ('question__refAuthor','question',)
    ordering = ('-createdDate',)
    search_fields=('choice_text','question__refAuthor__name','question__question_text')

    list_select_related = ('question','question__refAuthor',)
