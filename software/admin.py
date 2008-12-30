from django.contrib import admin
from software.models import Author,Tag,License,Language,OpSys,Software
from software.models import SoftwareRating,SoftwareStatistics

class AuthorAdmin(admin.ModelAdmin):
    pass

class TagAdmin(admin.ModelAdmin):
    pass

class LicenseAdmin(admin.ModelAdmin):
    pass
    
class LanguageAdmin(admin.ModelAdmin):
    pass

class OpSysAdmin(admin.ModelAdmin):
    pass

class SoftwareAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Metadata', {
        'fields': ('user', 'title', 'version', 'authors')}),
        ('None', {
            'fields': ( 'contact', 'short_description', 'description', 'changes',
            'project_url', 'jmlr_mloss_url', 'tags', 'language', 'os_license',
            'revision', 'updated_date', 'tarball', 'thumbnail', 'screenshot',
            'operating_systems', 'dataformats', 'paper_bib',
            'total_number_of_views', 'total_number_of_downloads')}),
        )
    list_filter = ['pub_date']
    date_hierarchy = 'pub_date'
    search_fields = ['title']

class SoftwareRatingAdmin(admin.ModelAdmin):
    list_display = ('software', 'user', 'features', 'usability', 'documentation')

class SoftwareStatisticsAdmin(admin.ModelAdmin):
    list_display = ('software', 'date', 'number_of_views', 'number_of_downloads')

admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(OpSys, OpSysAdmin)
admin.site.register(Software, SoftwareAdmin)
admin.site.register(SoftwareRating, SoftwareRatingAdmin)
admin.site.register(SoftwareStatistics, SoftwareStatisticsAdmin)
