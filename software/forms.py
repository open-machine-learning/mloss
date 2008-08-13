"""
Forms for adding Software

"""
from django.conf import settings
from django import forms
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.views.generic.create_update import update_object
from django.forms.widgets import RadioSelect
from django.utils.html import strip_tags
from StringIO import StringIO  
from software.models import Software, Language, License, Tag, Author, OpSys
import software.views.list
import re

version_re = re.compile(r'^[a-zA-Z0-9\.\- ]+$')
authors_re = re.compile(r'^[a-zA-Z ,\.]+$')
title_re = re.compile(r'^[a-zA-Z0-9 ,\.]+$')
tags_re = re.compile(r'^[a-z0-9 ,]+$')
os_license_re = re.compile(r'^[a-zA-Z0-9\. ,]+$')
language_re = re.compile(r'^[a-zA-Z\+ ,]+$')
os_re = re.compile(r'^[a-zA-Z ,]+$')
bib_re = re.compile(r'^[a-zA-Z{}@, \+ ,]+$')

from models import Software, editables, dontupdateifempty

class UpdateSoftwareForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UpdateSoftwareForm, self).__init__(*args, **kwargs)
        self.fields['authors_choice'].choices = [('', '')] + [
                (x.id, x.name) for x in Author.objects.all().order_by('name')]
        self.fields['language_choice'].choices = [('', '')] + [
                (x.id, x.name) for x in Language.objects.all().order_by('name')]
        self.fields['tags_choice'].choices = [('', '')] + [
                (x.id, x.name) for x in Tag.objects.all().order_by('name')]
        self.fields['os_license_choice'].choices = [('', '')] + [
                (x.id, x.name) for x in License.objects.all().order_by('name')]
        self.fields['operating_systems_choice'].choices = [('', '')] + [
                (x.id, x.name) for x in OpSys.objects.all().order_by('name')]

    #title = forms.CharField(widget=forms.HiddenInput(), label=u'')
    title = forms.CharField(max_length=80,
            widget=forms.TextInput(attrs={'size' : '30', 'readonly' : 'readonly'}),
            label=u'Title', required=True, help_text=u'(read only)')
    version = forms.CharField(max_length=80,
            widget=forms.TextInput(attrs={'size' : '20'}), label=u'Version',
            help_text=u'(required)')
    authors = forms.CharField(max_length=200, 
            widget=forms.TextInput(attrs={'size' : '20'}), label=u'Authors',
            help_text=u'(required) A comma seperated list, up to 200 characters long')
    authors_choice = forms.ChoiceField(widget=forms.Select(attrs={'size' : 1}), required=False)
    
    contact = forms.EmailField(max_length=80, 
            widget=forms.TextInput(attrs={'size' : '30'}), label=u"Main Author's Email Address",
            help_text=u'(required)')
    description = forms.CharField(
            widget=forms.Textarea(attrs={"rows":15, "cols":70}), label=u'Description',
            help_text=u'(required) The first paragraph, truncated at 200 characters, is displayed as the summary')
    project_url = forms.URLField(
            widget=forms.TextInput(attrs={'size' : '30'}),
            label=u'Project Homepage', required=False,
            help_text=u'Project Homepage URL')
    tags = forms.CharField(widget=forms.TextInput(attrs={'size' : '20'}),
            label=u'Tags', required=False,
            help_text=u'A comma seperated list of keywords')
    tags_choice = forms.ChoiceField(widget=forms.Select(attrs={'size' : 1}), required=False)

    language = forms.CharField(max_length=200,
            widget=forms.TextInput(attrs={'size' : '20'}), label=u'Programming Language(s)',
            help_text=u'(required) A comma seperated list, up to 200 characters long')
    language_choice = forms.ChoiceField(widget=forms.Select(attrs={'size' : 1}), required=False)

    os_license = forms.CharField(max_length=200,
            widget=forms.TextInput(attrs={'size' : '20'}), label=u'Open Source License',
            help_text=u'(required) A comma seperated list, up to 200 characters long')
    os_license_choice = forms.ChoiceField(widget=forms.Select(attrs={'size' : 1}), required=False)

    tarball = forms.FileField(widget=forms.FileInput(attrs={'size' : '20'}),
            label=u'Project Archive', required=False,
            help_text=u'(required) Archive or direct download link')
    download_url = forms.URLField(
            widget=forms.TextInput(attrs={'size' : '30'}),
            label=u'Download URL', required=False,
            help_text=u'(required) Archive or direct download link')
    screenshot = forms.ImageField(widget=forms.FileInput(attrs={'size' : '20'}),
            label=u'Screenshot', required=False,
            help_text=u'Limited to 1280x1024 pixels and less than 200K; .png, .jpg or .gif only.')
    paper_bib = forms.CharField(
            widget=forms.Textarea(attrs={"rows":5, "cols":70}), label=u'Corresponding paper',
            required=False, help_text=u'BibTeX entry of a corresponding paper.')

    operating_systems = forms.CharField(widget=forms.TextInput(attrs={'size' : '20'}),
            label=u'Operating Systems',
            help_text=u'(required) A comma seperated list of supported OSes')
    operating_systems_choice = forms.ChoiceField(widget=forms.Select(attrs={'size' : 1}), required=False)

    def clean_version(self):
        """
        Validates that version is alphanumeric
        """
        if 'version' in self.cleaned_data:
            if not version_re.search(self.cleaned_data['version']):
                raise forms.ValidationError(u'Version may only contain letters, numbers, minus, dots and spaces.')
            else:
                return self.cleaned_data['version']

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

    def clean_tarball(self):
        """
        Check that archive is only .tar.gz .tar.bz2 .zip 
        """
        if 'tarball' in self.data:
            tarball = self.data['tarball']
            if tarball and tarball.get('content-type') not in ('application/zip',
                    'application/gzip', 
                    'application/x-gzip', 
                    'application/tar', 
                    'application/x-tar', 
                    'application/x-gzip', 
                    'application/x-bzip', 
                    'application/x-bzip-compressed-tar'):
                raise forms.ValidationError(u'Only compressed or uncompressed zip or tar archives allowed.')
            if len(tarball['content']) > settings.MAX_FILE_UPLOAD_SIZE * 1024:
                raise forms.ValidationError(u'Tarball too big, max allowed size is %d KB' % settings.MAX_FILE_UPLOAD_SIZE)

        return self.cleaned_data['tarball']

    def clean_screenshot(self):
        """
        Check that screenshot is only jpeg/png/gif
        """
        if 'screenshot' in self.data:
            screenshot = self.data['screenshot']
            if screenshot and screenshot.get('content-type') not in ('image/jpeg',
                    'image/gif', 'image/png', 'image/x-png', 'image/pjpeg'):
                raise forms.ValidationError(u'Only images of type png, gif or jpeg allowed.')

            if len(screenshot['content']) > settings.MAX_IMAGE_UPLOAD_SIZE * 1024:
                raise forms.ValidationError(u'Image too big, max allowed size is %d KB' % settings.MAX_IMAGE_UPLOAD_SIZE)

            try:
                from PIL import Image  
                img = Image.open(StringIO(screenshot['content']))  
                width, height = img.size
                if width > settings.MAX_IMAGE_UPLOAD_WIDTH:
                    raise forms.ValidationError('Maximum image width is %s' % settings.MAX_IMAGE_UPLOAD_WIDTH)
                if height > settings.MAX_IMAGE_UPLOAD_HEIGHT:
                    raise forms.ValidationError('Maximum image height is %s' % settings.MAX_IMAGE_UPLOAD_HEIGHT)
            except ImportError:
                pass

        return self.cleaned_data['screenshot']

    def clean_operating_systems(self):
        """
        Validates that operating system is alphanumeric, comma, whitespace
        """
        if 'operating_systems' in self.cleaned_data:
            if not os_re.search(self.cleaned_data['operating_systems']):
                raise forms.ValidationError(u'Operating system must be comma separated names and may only contain letters and spaces.')
        return self.cleaned_data['operating_systems']

    def clean(self):
        """
        Make sure that download url or tarball are given
        """
        err_msg=u'Either Project Archive or Download URL Required.'

        # when both items are given raise an error
        if ('tarball' in self.data and self.data['tarball']) and ('download_url' in self.data and self.data['download_url']):
            self._errors['tarball'] = [err_msg]
            self._errors['download_url'] = [err_msg]
            raise forms.ValidationError(err_msg)

        # check whether a tarball is already stored
        has_tarball = False
        if 'title' in self.data:
            try:
                sw = Software.objects.get(title__exact=self.data['title'])
                has_tarball = sw.tarball and not ('download_url' in self.data and self.data['download_url'])
            except Software.DoesNotExist:
                pass

        # if neither current software has a tarball nor has a tarball in the form nor has a 
        # download url raise an error
        if not ( has_tarball or ('tarball' in self.data and self.data['tarball']) or ('download_url' in self.data and self.data['download_url'])):
            self._errors['tarball'] = [err_msg]
            self._errors['download_url'] = [err_msg]
            raise forms.ValidationError(err_msg)

        return self.cleaned_data

class SoftwareForm(UpdateSoftwareForm):
    title = forms.CharField(max_length=80,
            widget=forms.TextInput(attrs={'size' : '30'}),
            label=u'Title', required=True, help_text=u'(required) Up to 80 characters long')

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
                                    operating_systems = form.cleaned_data['operating_systems'],
                                    os_license=form.cleaned_data['os_license'],
                                    paper_bib = form.cleaned_data['paper_bib'],
                                    download_url=form.cleaned_data['download_url'],
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
        return software.views.list.search_description(request, q)
    else:
        return HttpResponseRedirect('/software')

def edit_software(request, software_id):
    """
    Show the software form, and capture the information
    """


    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login?next=%s' % request.path)

    if request.user.is_superuser:
        software = get_object_or_404(Software,
                pk=software_id)
    else:
        software = get_object_or_404(Software,
                pk=software_id,
                user__pk=request.user.id)

    if request.method == 'POST':
        new_data = request.POST.copy()
        new_data.update(request.FILES)
        form = UpdateSoftwareForm(new_data)

        if form.is_valid():
            for field in editables:
                if not field in dontupdateifempty or form.cleaned_data[field]:
                    setattr(software, field, form.cleaned_data[field])

            if form.cleaned_data['download_url'] and len(form.cleaned_data['download_url'])>0:
                software.tarball = None
            else:
                save_tarball(request, software)
            save_screenshot(request, software)
            software.save()
            return HttpResponseRedirect(software.get_absolute_url())
    else:
        form = UpdateSoftwareForm(software)

    return render_to_response('software/software_add.html',
                              { 'form': form },
                              context_instance=RequestContext(request))

class RatingForm(forms.Form):
    features = forms.IntegerField(widget=RadioSelect(choices=( (0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5') )))
    usability = forms.IntegerField(widget=RadioSelect(choices=( (0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5') )))
    documentation = forms.IntegerField(widget=RadioSelect(choices=( (0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5') )))
