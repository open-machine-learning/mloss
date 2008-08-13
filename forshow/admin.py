from django.contrib import admin
from forshow.models import News, Faq

class NewsAdmin(admin.ModelAdmin):
    list_display = ('headline', 'publication_date')

class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
    fieldsets = (
            (None, {'fields': ('question','answer')}),
            )


admin.site.register(News, NewsAdmin)
admin.site.register(Faq, FaqAdmin)
