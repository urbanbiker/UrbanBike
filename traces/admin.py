from django.contrib import admin

from traces.models import Trace

class TraceAdmin(admin.ModelAdmin):
    list_display = ('id', "uuid", "title", 'user', 'created')
    raw_id_fields = ('user', )
    search_fields = ('uuid', )

admin.site.register(Trace, TraceAdmin)

