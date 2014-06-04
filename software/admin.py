from django.contrib import admin
from software.models import Software
from software.models import SoftwareRating,SoftwareStatistics

class SoftwareAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Metadata', {
        'fields': ('user', 'title')}),
        ('None', {
            'fields': ( 'total_number_of_views', 'total_number_of_downloads')}),
        )
    search_fields = ['title']

class SoftwareRatingAdmin(admin.ModelAdmin):
    list_display = ('software', 'user', 'features', 'usability', 'documentation')

class SoftwareStatisticsAdmin(admin.ModelAdmin):
    list_display = ('software', 'date', 'number_of_views', 'number_of_downloads')

admin.site.register(Software, SoftwareAdmin)
admin.site.register(SoftwareRating, SoftwareRatingAdmin)
admin.site.register(SoftwareStatistics, SoftwareStatisticsAdmin)
