from django.contrib import admin
from registration.models import RegistrationProfile

class RegistrationProfileAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'activation_key_expired')
	search_fields = ('user__username', 'user__first_name')

admin.site.register(RegistrationProfile, RegistrationProfileAdmin)
