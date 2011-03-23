"""
Forms for adding Software

"""
from django.conf import settings
from django import forms
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.create_update import update_object
from django.forms.widgets import RadioSelect, Textarea
from django.utils.html import strip_tags
from django.core.mail import send_mail
import django.core.files.base

from StringIO import StringIO  
from software.models import Software
from revision.models import Revision
from revision.models import Language, License, Tag, Author, OpSys, DataFormat
from revision.models import editables, dontupdateifempty
import software.views.list
import re
from PIL import Image
import os.path


version_re = re.compile(r'^[a-zA-Z0-9\.\- ]+$')
authors_re = re.compile(r'^[a-zA-Z ,\.]+$')
title_re = re.compile(r'^[a-zA-Z0-9 ,\.]+$')
tags_re = re.compile(r'^[a-z0-9 ,]+$')
os_license_re = re.compile(r'^[a-zA-Z0-9\. ,]+$')
language_re = re.compile(r'^[a-zA-Z\+ ,]+$')
os_re = re.compile(r'^[a-zA-Z ,]+$')
bib_re = re.compile(r'^[a-zA-Z{}@, \+ ,]+$')

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
        self.fields['dataformats_choice'].choices = [('', '')] + [
                (x.id, x.name) for x in DataFormat.objects.all().order_by('name')]

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
    short_description = forms.CharField(
            widget=forms.Textarea(attrs={"rows":2, "cols":70}), label=u'Short Description',
            help_text=u'(required) A brief summary that will be displayed in the software listing.')
    description = forms.CharField(
            widget=forms.Textarea(attrs={"rows":15, "cols":70}), label=u'Description',
            help_text=u'(required) An extended description of the software')
    changes = forms.CharField(
            widget=forms.Textarea(attrs={"rows":5, "cols":70}), label=u'Changes since last revision',
            help_text=u'(required) A summary of the changes since the previous release.')
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
    thumbnail = forms.ImageField(widget=forms.FileInput(attrs={'size' : '20'}),
            label=u'Thumbnail', required=False,
            help_text=u'Icon shown in software list; 30x32 pixels; .png, .jpg or .gif only.')
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
    dataformats = forms.CharField(widget=forms.TextInput(attrs={'size' : '20'}),
            label=u'Data Formats',
            help_text=u'(required) A comma seperated list of supported Data Formats')
    dataformats_choice = forms.ChoiceField(widget=forms.Select(attrs={'size' : 1}), required=False)

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
        if 'tarball' in self.data and len(self.data['tarball']):
            tarball = self.data['tarball']

            if tarball and tarball.content_type not in ('application/zip',
                    'application/x-zip',
                    'application/x-zip-compressed',
                    'application/x-compress',
                    'application/x-compressed',
                    'application/gzip', 
                    'application/x-gzip', 
                    'application/tar', 
                    'application/x-tar', 
                    'application/x-bzip', 
                    'application/bzip2', 
                    'application/x-bzip-compressed-tar'):
                raise forms.ValidationError(u'Only compressed or uncompressed zip or tar archives allowed, got "%s".' % tarball.content_type)
            if tarball.size > settings.MAX_FILE_UPLOAD_SIZE * 1024:
                raise forms.ValidationError(u'Tarball too big, max allowed size is %d KB' % settings.MAX_FILE_UPLOAD_SIZE)

        return self.cleaned_data['tarball']

    def clean_thumbnail(self):
        """
        Check that thumbnail is only jpeg/png/gif
        """
        if 'thumbnail' in self.data and len(self.data['thumbnail']):
            thumbnail = self.data['thumbnail']

            if thumbnail and thumbnail.content_type not in ('image/jpeg',
                    'image/gif', 'image/png', 'image/x-png', 'image/pjpeg'):
                raise forms.ValidationError(u'Only images of type png, gif or jpeg allowed.')

            if thumbnail.size > settings.MAX_IMAGE_UPLOAD_SIZE * 1024:
                raise forms.ValidationError(u'Image too big, max allowed size is %d KB' % settings.MAX_IMAGE_UPLOAD_SIZE)

            try:
                from PIL import Image  
                img = Image.open(StringIO(thumbnail.read()))
                thumbnail.open() # seek to beginning of file
                width, height = img.size
                if width != 30:
                    raise forms.ValidationError('Image must be 30 pixels wide')
                if height != 32:
                    raise forms.ValidationError('Image must be 32 pixels in height')
            except ImportError:
                pass

        return self.cleaned_data['thumbnail']

    def clean_screenshot(self):
        """
        Check that screenshot is only jpeg/png/gif
        """
        if 'screenshot' in self.data and len(self.data['screenshot']):
            screenshot = self.data['screenshot']

            if screenshot and screenshot.content_type not in ('image/jpeg',
                    'image/gif', 'image/png', 'image/x-png', 'image/pjpeg'):
                raise forms.ValidationError(u'Only images of type png, gif or jpeg allowed.')

            if screenshot.size > settings.MAX_IMAGE_UPLOAD_SIZE * 1024:
                raise forms.ValidationError(u'Image too big, max allowed size is %d KB' % settings.MAX_IMAGE_UPLOAD_SIZE)

            try:
                from PIL import Image  
                img = Image.open(StringIO(screenshot.read()))
                screenshot.open() # seek to beginning of file
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

    def clean_dataformats(self):
        """
        Validates that dataformats are alphanumeric, comma, whitespace
        """
        if 'dataformats' in self.cleaned_data:
            if not os_re.search(self.cleaned_data['dataformats']):
                raise forms.ValidationError(u'Data Formats must be comma separated names and may only contain letters and spaces.')
        return self.cleaned_data['dataformats']

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
                rev= Revision.objects.get(software__exact=sw, revision=0)
                has_tarball = rev.tarball and not ('download_url' in self.data and self.data['download_url'])
            except Software.DoesNotExist:
                pass
            except Revision.DoesNotExist:
                pass

        # if neither current software has a tarball nor has a tarball in the form nor has a 
        # download url raise an error
        if not ( has_tarball or ('tarball' in self.data and self.data['tarball']) or ('download_url' in self.data and self.data['download_url'])):
            self._errors['tarball'] = [err_msg]
            self._errors['download_url'] = [err_msg]
            raise forms.ValidationError(err_msg)

        return self.cleaned_data

class RevisionForm(UpdateSoftwareForm):
    version = forms.CharField(max_length=80,
            widget=forms.TextInput(attrs={'size' : '20', 'readonly' : 'readonly'}),
            label=u'Version', help_text=u'(required)')

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
        filename = request.FILES['tarball'].name
        object.tarball.save(filename, request.FILES['tarball'], save=False)

def make_thumbnail(buf, size=(30, 32)):
    f = StringIO(buf)
    image = Image.open(buf)
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')
    image.thumbnail(size, Image.ANTIALIAS)
    o = StringIO()
    image.save(o, 'JPEG') 
    return o.getvalue()

def save_images(request, new_revision, old_revision=None):
    '''
    Saves both screenshot and thumbnail. 
    '''
    newThumb      = request.FILES.has_key('thumbnail')
    newScreenshot = request.FILES.has_key('screenshot')
    
    if newThumb and not newScreenshot:
        if old_revision != None:
            new_revision.screenshot = old_revision.screenshot
        new_revision.thumbnail.save(request.FILES['thumbnail'].name, content=request.FILES['thumbnail'], save=False)
    elif not newThumb and newScreenshot:
        new_revision.screenshot.save(request.FILES['screenshot'].name, content=request.FILES['screenshot'], save=False)
        if old_revision != None:
            new_revision.thumbnail = old_revision.thumbnail        
    elif newThumb and newScreenshot:
        new_revision.screenshot.save(request.FILES['screenshot'].name, content=request.FILES['screenshot'], save=False)
        new_revision.thumbnail.save(request.FILES['thumbnail'].name, content=request.FILES['thumbnail'], save=False)
    else:
        if old_revision != None:
            new_revision.thumbnail = old_revision.thumbnail            
            new_revision.screenshot = old_revision.screenshot
            
    if new_revision.thumbnail == None and new_revision.screenshot != None:
        screenshotName = request.FILES['screenshot'].name
        screenshot     = request.FILES['screenshot']
        thumbnailName  = '%s.thumb.jpg' % os.path.splitext(screenshotName)[0]
        thumbnail      = django.core.files.base.ContentFile(make_thumbnail(screenshot, size=(30,32)))
        new_revision.thumbnail.save(thumbnailName, content=thumbnail, save=False)


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
                                    title=form.cleaned_data['title'])
            if original_id:
                new_software.original_id = original_id
            new_software.save()

            try:
                new_revision = Revision(software=new_software,
                                        version=form.cleaned_data['version'],
                                        authors=form.cleaned_data['authors'],
                                        contact=form.cleaned_data['contact'],
                                        short_description=form.cleaned_data['short_description'],
                                        description=form.cleaned_data['description'],
                                        changes='Initial Announcement on mloss.org.',
                                        project_url=form.cleaned_data['project_url'],
                                        tags=form.cleaned_data['tags'],
                                        language=form.cleaned_data['language'],
                                        operating_systems = form.cleaned_data['operating_systems'],
                                        dataformats = form.cleaned_data['dataformats'],
                                        os_license=form.cleaned_data['os_license'],
                                        paper_bib = form.cleaned_data['paper_bib'],
                                        download_url=form.cleaned_data['download_url'],
                                        tarball=form.cleaned_data['tarball'],
                                        thumbnail=form.cleaned_data['thumbnail'],
                                        screenshot=form.cleaned_data['screenshot'],
                                        )
                if original_id:
                    new_revision.original_id = original_id

                save_tarball(request, new_revision)
                save_images(request, new_revision, old_revision = None)
                new_revision.save()
                return HttpResponseRedirect(new_revision.get_absolute_url())
            except:
                new_software.delete()
    else:
        form = SoftwareForm(initial={'user':request.user,
            'changes':'Initial Announcement on mloss.org.'})

    return render_to_response('software/software_add.html',
                              { 'form': form },
                              context_instance=RequestContext(request))

class SearchForm(forms.Form):
    searchterm = forms.CharField(max_length=40)

def search_software(request):
    searchform = SearchForm()

    if request.method == 'GET':
        try:
            q = request.GET['searchterm'];
            return software.views.list.search_description(request, q)
        except:
            return HttpResponseRedirect('/software')
    else:
        return HttpResponseRedirect('/software')

def edit_software(request, software_id, revision_id=0):
    """
    Show the software form, and capture the information
    """

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login?next=%s' % request.path)

    original_id = request.GET.get('oid', None)

    if request.user.is_superuser:
        software = get_object_or_404(Software,
                pk=software_id)
    else:
        software = get_object_or_404(Software,
                pk=software_id,
                user__pk=request.user.id)

    if revision_id:
        revision = get_object_or_404(Revision,
                pk=revision_id, software = software)
        form_class = RevisionForm
    else:
        revision = software.get_latest_revision()
        form_class = UpdateSoftwareForm

    if request.method == 'POST':
        new_data = request.POST.copy()
        new_data.update(request.FILES)
        form = form_class(new_data)

        if form.is_valid():
            if form.cleaned_data['title'] != software.title or ( revision_id
                    and form.cleaned_data['version'] != revision.version ):
                return HttpResponseForbidden()

            new_revision = Revision(software=software,
                                    version=form.cleaned_data['version'],
                                    authors=form.cleaned_data['authors'],
                                    contact=form.cleaned_data['contact'],
                                    short_description=form.cleaned_data['short_description'],
                                    description=form.cleaned_data['description'],
                                    changes=form.cleaned_data['changes'],
                                    project_url=form.cleaned_data['project_url'],
                                    tags=form.cleaned_data['tags'],
                                    language=form.cleaned_data['language'],
                                    operating_systems = form.cleaned_data['operating_systems'],
                                    dataformats = form.cleaned_data['dataformats'],
                                    os_license=form.cleaned_data['os_license'],
                                    paper_bib = form.cleaned_data['paper_bib'],
                                    download_url=form.cleaned_data['download_url'],
                                    tarball=form.cleaned_data['tarball'],
                                    thumbnail=form.cleaned_data['thumbnail'],
                                    screenshot=form.cleaned_data['screenshot'],
                                    )
            if original_id:
                new_revision.original_id = original_id

            if new_revision.version != revision.version:
                for field in editables:
                    if not field in dontupdateifempty or form.cleaned_data[field]:
                        setattr(new_revision, field, form.cleaned_data[field])

                if form.cleaned_data['download_url'] and len(form.cleaned_data['download_url'])>0:
                    new_revision.tarball = None
                else:
                    save_tarball(request, new_revision)

                save_images(request, new_revision, old_revision=revision)
                software.increment_revisions()
                new_revision.save()
                return HttpResponseRedirect(new_revision.get_absolute_url())
            else:
                for field in editables:
                    if not field in dontupdateifempty or form.cleaned_data[field]:
                        setattr(revision, field, form.cleaned_data[field])

                if form.cleaned_data['download_url'] and len(form.cleaned_data['download_url'])>0:
                    revision.tarball = None
                else:
                    save_tarball(request, revision)

                save_images(request, revision, old_revision = revision)
                revision.save(silent_update=True)
                return HttpResponseRedirect(revision.get_absolute_url())
    else:
        form = form_class(revision)

    return render_to_response('software/software_add.html',
                              { 'form': form },
                              context_instance=RequestContext(request))



class RatingForm(forms.Form):
    features = forms.IntegerField(widget=RadioSelect(choices=( (0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5') )))
    usability = forms.IntegerField(widget=RadioSelect(choices=( (0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5') )))
    documentation = forms.IntegerField(widget=RadioSelect(choices=( (0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5') )))



class AuthorContactForm(forms.Form):
    subject   = forms.CharField(max_length=100, label='Subject')
    message   = forms.CharField(label='Your message', widget=Textarea)
    cc_myself = forms.BooleanField(required=False, label='Send email CC: to you')

def contact_author(request, software_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login?next=%s' % request.path)
        
    if request.method == 'POST': # If the form has been submitted...
        form = AuthorContactForm(request.POST) # A form bound to the POST data
        software = get_object_or_404(Software, pk=software_id)
        if form.is_valid(): # All validation rules pass
            subject    = form.cleaned_data['subject']
            message    = form.cleaned_data['message']
            sender     = request.user.email
            cc_myself  = form.cleaned_data['cc_myself']
            recipients = [software.get_latest_revision().contact,]
            if cc_myself:
                recipients.append(sender)
            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect(software.get_absolute_url())
    else:
        form = AuthorContactForm() # An unbound form

    return render_to_response('software/software_contact_author.html', { 'form': form }, context_instance=RequestContext(request))    