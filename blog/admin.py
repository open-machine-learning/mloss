from django.contrib import admin
from blog.models import BlogItem

class BlogItemAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'headline', 'author')


admin.site.register(BlogItem, BlogItemAdmin)

