"""
Forms for adding Software

"""
from django import newforms as forms
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.views.generic.create_update import update_object
import software.views.entry

from models import Software, editables, dontupdateifempty

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

def create_form():
    return forms.form_for_model(Software, formfield_callback=form_callback, fields=editables)

def add_software(request):
    """
    Show the software form, and capture the information
    """

    if not request.user.is_authenticated():
       return HttpResponseRedirect('/accounts/login?next=%s' % request.path)

    AddSoftwareForm = create_form()

    original_id = request.GET.get('oid', None)

    if request.method == 'POST':
        new_data = request.POST.copy()
        new_data.update(request.FILES)
        form = AddSoftwareForm(new_data)
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
        form = AddSoftwareForm(initial={'user':request.user})

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
