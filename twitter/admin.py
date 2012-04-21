from django.contrib import admin
from twitter.models import Search

class SearchAdmin(admin.ModelAdmin):
    list_display = ("query",)

admin.site.register(Search, SearchAdmin)
