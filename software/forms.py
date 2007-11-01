"""
Forms for adding Software

"""
from django import newforms as forms
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.views.generic.create_update import update_object
from django.newforms.widgets import RadioSelect
from django.utils.html import strip_tags
from software.models import Software
import software.views.entry
import re

title_re = re.compile(r'^\w+$')
authors_re = re.compile(r'^[a-zA-Z ,]+$')
tags_re = re.compile(r'^[a-z0-9 ,]+$')
os_license_re = re.compile(r'^[a-zA-Z0-9 ,]+$')
language_re = re.compile(r'^[a-zA-Z\+ ,]+$')

from models import Software, editables, dontupdateifempty

class SoftwareForm(forms.Form):
    title = forms.CharField(max_length=80,
            widget=forms.TextInput(attrs={'size' : '30'}),
            label=u'Title', required=True) 
    version = forms.CharField(max_length=80,
            widget=forms.TextInput(attrs={'size' : '30'}), label=u'Version')
    authors = forms.CharField(max_length=200, 
            widget=forms.TextInput(attrs={'size' : '60'}), label=u'Authors')
    contact = forms.EmailField(max_length=80, 
        widget=forms.TextInput(attrs={'size' : '60'}), label=u"Main Author's Email Address:")
    description = forms.CharField(
            widget=forms.Textarea(attrs={"rows":30, "cols":80}), label=u'Description')
    project_url = forms.URLField(
            widget=forms.TextInput(attrs={'size' : '60'}),
            label=u'Project Homepage', required=False)
    tags = forms.CharField(widget=forms.TextInput(attrs={'size' : '60'}),
            label=u'Tags', required=False)
    language = forms.CharField(max_length=200,
            widget=forms.TextInput(attrs={'size' : '60'}), label=u'Programming Language(s)')
    os_license = forms.CharField(max_length=200,
            widget=forms.TextInput(attrs={'size' : '60'}), label=u'Title')
    tarball = forms.FileField(widget=forms.FileInput(attrs={'size' : '30'}),
            label=u'Project Archive', required=False)
    screenshot = forms.ImageField(widget=forms.FileInput(attrs={'size' : '30'}),
            label=u'Screenshot', required=False)

    def clean_title(self):
        """
        Validates that title is alphanumeric
        """
        if 'title' in self.cleaned_data:
            if not title_re.search(self.cleaned_data['title']):
                raise forms.ValidationError(u'Title may only contain letters, numbers and underscores')
            try:
                sw = Software.objects.get(title__exact=self.cleaned_data['title'])
            except Software.DoesNotExist:
                return self.cleaned_data['title']
            raise forms.ValidationError(u'This software project title is already taken. Please choose another name.')

    def clean_authors(self):
        """
        Validates that author names are alphanumeric
        """
        if 'authors' in self.cleaned_data:
            if not authors_re.search(self.cleaned_data['authors']):
                raise forms.ValidationError(u'Author names may only contain letters, comma and spaces.')
            else:
                return self.cleaned_data['authors']

    def clean_tags(self):
        """
        Validates that tags are lowercase alphanumeric
        """
        if 'tags' in self.cleaned_data and self.cleaned_data['tags'] and not tags_re.search(self.cleaned_data['tags']):
                raise forms.ValidationError(u'Tags must be comma separated names and may only contain lowercase letters and spaces.')
        return self.cleaned_data['tags']

    def clean_os_license(self):
        """
        Validates that license is lowercase alphanumeric
        """
        if 'os_license' in self.cleaned_data:
            if not os_license_re.search(self.cleaned_data['os_license']):
                raise forms.ValidationError(u'License must be comma separated license names and may only contain letters, numbers and spaces.')
        return self.cleaned_data['os_license']

    def clean_language(self):
        """
        Validates that language is alphanumeric/plus, comma, whitespace
        """
        if 'language' in self.cleaned_data:
            if not language_re.search(self.cleaned_data['language']):
                raise forms.ValidationError(u'Language must be comma separated language names and may only contain letters, plusses and spaces.')
        return self.cleaned_data['language']

def save_tarball(request, object):
    """
    Retrieve filename and save the file
    """
    if request.FILES.has_key('tarball'):
        filename = request.FILES['tarball']['filename']
        object.save_tarball_file(filename, request.FILES['tarball']['content'])

def save_screenshot(request, object):
    """
    Retrieve filename and save the file
    """
    if request.FILES.has_key('screenshot'):
        filename = request.FILES['screenshot']['filename']
        object.save_screenshot_file(filename, request.FILES['screenshot']['content'])

def form_callback(f, **kw):
    if f.name == 'description':
        return forms.CharField(widget=forms.Textarea(attrs={"rows":30, "cols":80}))
    elif f.name in ('tags', 'authors', 'contact', 'project_url'):
        return forms.CharField(widget=forms.TextInput(attrs={'size':'60'}), required=not f.blank)
    return f.formfield(**kw)

def add_software(request):
    """
    Show the software form, and capture the information
    """

    if not request.user.is_authenticated():
       return HttpResponseRedirect('/accounts/login?next=%s' % request.path)

    original_id = request.GET.get('oid', None)

    if request.method == 'POST':
        new_data = request.POST.copy()
        new_data.update(request.FILES)
        form = SoftwareForm(new_data)
        if form.is_valid():
            new_software = Software(user=request.user,
                                    title=form.cleaned_data['title'],
                                    version=form.cleaned_data['version'],
                                    authors=form.cleaned_data['authors'],
                                    contact=form.cleaned_data['contact'],
                                    description=form.cleaned_data['description'],
                                    project_url=form.cleaned_data['project_url'],
                                    tags=form.cleaned_data['tags'],
                                    language=form.cleaned_data['language'],
                                    os_license=form.cleaned_data['os_license'],
                                    tarball=form.cleaned_data['tarball'],
                                    screenshot=form.cleaned_data['screenshot'],
                                    )
            if original_id:
                new_software.original_id = original_id

            save_tarball(request, new_software)
            save_screenshot(request, new_software)
            new_software.save()
            return HttpResponseRedirect(new_software.get_absolute_url())
    else:
        form = SoftwareForm(initial={'user':request.user})

    return render_to_response('software/software_add.html',
                              { 'form': form },
                              context_instance=RequestContext(request))

class SearchForm(forms.Form):
    searchterm = forms.CharField(max_length=40)

def search_software(request):
    searchform = SearchForm()

    if request.method == 'POST':
        q = request.POST['searchterm'];
        return software.views.entry.search_description(request, q)
    else:
        return HttpResponseRedirect('/software')

def edit_software(request, software_id):
    """
    Show the software form, and capture the information
    """


    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login?next=%s' % request.path)

    EditSoftwareForm = create_form()

    if request.user.is_superuser:
        software = get_object_or_404(Software,
                pk=software_id)
    else:
        software = get_object_or_404(Software,
                pk=software_id,
                user__pk=request.user.id)

    if request.method == 'POST':
        form = EditSoftwareForm(request.POST)
        if form.is_valid():
            for field in editables:
                if not field in dontupdateifempty or form.cleaned_data[field]:
                    setattr(software, field, form.cleaned_data[field])

            save_tarball(request, software)
            save_screenshot(request, software)
            software.save()
            return HttpResponseRedirect(software.get_absolute_url())
    else:
        form = EditSoftwareForm(software)

    return render_to_response('software/software_add.html',
                              { 'form': form },
                              context_instance=RequestContext(request))

class RatingForm(forms.Form):
    features = forms.IntegerField(widget=RadioSelect(choices=( (0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5') )))
    usability = forms.IntegerField(widget=RadioSelect(choices=( (0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5') )))
    documentation = forms.IntegerField(widget=RadioSelect(choices=( (0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5') )))
    #features = forms.IntegerField()
    #usability = forms.IntegerField()
    #documentation = forms.IntegerField()
