from django.contrib import admin
from revision.models import Revision
from revision.models import Author,Tag,License,Language,OpSys

class RevisionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Metadata', {
        'fields': ('software', 'version', 'authors')}),
        ('None', {
            'fields': ( 'contact', 'short_description', 'description', 'changes',
            'project_url', 'jmlr_mloss_url', 'tags', 'language', 'os_license',
            'revision', 'updated_date', 'tarball', 'thumbnail', 'screenshot',
            'operating_systems', 'dataformats', 'paper_bib')}),
        )
    list_filter = ['pub_date', 'revision']
    date_hierarchy = 'pub_date'
    search_fields = ['software']
    list_display = ['software', 'version', 'changes', 'revision']


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

admin.site.register(Revision, RevisionAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(OpSys, OpSysAdmin)
