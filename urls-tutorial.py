from django.conf.urls.defaults import *
from mloss1.tutorial import current_datetime, hours_ahead, current_datetime_template
from mloss1.tutorial import current_datetime_short

urlpatterns = patterns('',
#                       (r'^now/$', current_datetime),
#                       (r'^now/$', current_datetime_template),
                       (r'^now/$', current_datetime_short),
                       (r'^now/plus(\d{1,2})hours/$', hours_ahead),
    # Example:
    # (r'^mloss1/', include('mloss1.foo.urls')),

                       # Uncomment this for admin:
                       (r'^admin/', include('django.contrib.admin.urls')),

                       # Using cab
                       (r'^software/', include('cab.urls')),

                       # Using registration
                       (r'^accounts/', include('registration.urls')),
)

