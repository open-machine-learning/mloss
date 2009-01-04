from django.views.generic.list_detail import object_list
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import Http404

from revision.models import Revision
from subscriptions.models import Subscriptions
import re

attrs_dict = { 'class': 'required' }
username_re = re.compile(r'^\w+$')

class ChangeUserDetailsForm(forms.Form):
    """
    Form for registering a new user account.

    Validates that the password is entered twice and matches,
    and that the username is not already taken.

    """
    firstname = forms.CharField(max_length=30,
            widget=forms.TextInput(attrs=attrs_dict),
            label=u'First Name', required=False)
    lastname = forms.CharField(max_length=30,
            widget=forms.TextInput(attrs=attrs_dict),
            label=u'Last Name', required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
        max_length=200)),
        label=u'Email address')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict),
            label=u'Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict),
            label=u'Password (again, to catch typos)')

    def clean_firstname(self):
        """
        Validates that the first is alphanumeric
        """
        if 'firstname' in self.cleaned_data:
            if self.cleaned_data['firstname'] and not username_re.search(self.cleaned_data['firstname']):
                raise forms.ValidationError(u'First name can only contain letters, numbers and underscores')
        return self.cleaned_data['firstname']

    def clean_lastname(self):
        """
        Validates that the lastname is alphanumeric
        """
        if 'firstname' in self.cleaned_data:
            if self.cleaned_data['lastname'] and not username_re.search(self.cleaned_data['lastname']):
                raise forms.ValidationError(u'Last name can only contain letters, numbers and underscores')
        return self.cleaned_data['lastname']

    def clean_username(self):
        """
        Validates that the username is alphanumeric and is not already
        in use.

        """
        if 'username' in self.cleaned_data:
            if not username_re.search(self.cleaned_data['username']):
                raise forms.ValidationError(u'Usernames can only contain letters, numbers and underscores')
            try:
                user = User.objects.get(username__exact=self.cleaned_data['username'])
            except User.DoesNotExist:
                return self.cleaned_data['username']
            raise forms.ValidationError(u'This username is already taken. Please choose another.')

    def clean_password2(self):
        """
        Validates that the two password inputs match.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data and \
                self.cleaned_data['password1'] == self.cleaned_data['password2']:
                    return self.cleaned_data['password2']
        raise forms.ValidationError(u'You must type the same password each time')

    def save(self, u):
        u.first_name=self.cleaned_data['firstname']
        u.last_name=self.cleaned_data['lastname']
        u.email=self.cleaned_data['email']
        u.set_password(self.cleaned_data['password1'])
        u.save()

def show_user_list(request):
    if request.user.is_superuser:
        return object_list(request,
                paginate_by=10,
                queryset=User.objects.all(),
                template_name='users/user_list.html')
    raise Http404

def show_user(request, user_id):
    if request.user.is_authenticated():
        entry = get_object_or_404(User, pk=user_id)

        if not request.user.is_superuser and not entry == request.user:
            raise Http404

        form = ChangeUserDetailsForm(initial={ 'firstname' : entry.first_name,
            'lastname' : entry.last_name,
            'email' : entry.email,
            'password1' : entry.password,
            'password2' : entry.password })

        t = ContentType.objects.get(app_label="software", model="software")
        swsubscriptions = Subscriptions.objects.filter(user=request.user,
                bookmark=False, content_type=t)
        swbookmarks = Subscriptions.objects.filter(user=request.user,
                bookmark=True, content_type=t)
        t = ContentType.objects.get(app_label="community", model="forum")
        forumsubscriptions = Subscriptions.objects.filter(user=request.user,
                bookmark=False, content_type=t)
        forumbookmarks = Subscriptions.objects.filter(user=request.user,
                bookmark=True, content_type=t)
        t = ContentType.objects.get(app_label="community", model="thread")
        threadsubscriptions = Subscriptions.objects.filter(user=request.user,
                bookmark=False, content_type=t)
        threadbookmarks = Subscriptions.objects.filter(user=request.user,
                bookmark=True, content_type=t)

        return render_to_response('users/user_detail.html',
                { 'object': entry,
                    'softwares' : Revision.objects.get_by_submitter(entry.username),
                    'swsubscriptions' : swsubscriptions,
                    'swbookmarks' : swbookmarks,
                    'forumsubscriptions' : forumsubscriptions,
                    'forumbookmarks' : forumbookmarks,
                    'threadsubscriptions' : threadsubscriptions,
                    'threadbookmarks' : threadbookmarks,
                    'form' : form },
                context_instance=RequestContext(request))

    raise Http404

def update_user(request, user_id):
    if request.user.is_authenticated():
        entry = get_object_or_404(User, pk=user_id)

        if not request.user.is_superuser and not entry == request.user:
            raise Http404

        form = ChangeUserDetailsForm(initial={ 'firstname' : entry.first_name,
            'lastname' : entry.last_name,
            'email' : entry.email,
            'password1' : entry.password,
            'password2' : entry.password })

        if request.method == 'POST':
            form = ChangeUserDetailsForm(request.POST)
            if form.is_valid():
                form.save(entry)
                return render_to_response('users/user_change_done.html',
                        { 'object': entry},
                        context_instance=RequestContext(request))

        return render_to_response('users/user_detail.html',
                { 'object': entry,
                    'softwares' : Revision.objects.get_by_submitter(entry.username),
                    'form' : form,
                    },
                context_instance=RequestContext(request))

    raise Http404
