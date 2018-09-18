from django import forms
from registration.forms import RegistrationFormTermsOfService
from captcha.fields import ReCaptchaField
from django.conf import settings
from django.utils.encoding import smart_unicode, force_unicode
from django.utils.translation import ugettext_lazy as _
from django.forms.forms import BoundField
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

class RegistrationFormCaptcha(RegistrationFormTermsOfService):
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
