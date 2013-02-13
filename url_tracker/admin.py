from django.contrib import admin

from url_tracker.models import URLChangeRecord


class URLChangeRecordAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'deleted', 'date_changed')
    list_filter = ('deleted', 'date_changed')

admin.site.register(URLChangeRecord, URLChangeRecordAdmin)
