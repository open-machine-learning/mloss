"""
Forms for adding Software

"""
import datetime
from django import newforms as forms
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.generic.create_update import update_object

from models import Software

AddSoftwareForm = forms.form_for_model(Software)

def addsoftware(request):
    """
    Show the software form, and capture the information
    """

    if not request.user.is_authenticated():
       return HttpResponseRedirect('/accounts/login?next=%s' % request.path)

    def save_tarball(object):
        """
        Retrieve filename and save the file
        """
        if request.FILES.has_key('tarball'):
            filename = request.FILES['tarball']['filename']
            object.save_tarball_file(filename, request.FILES['tarball']['content'])

    
    original_id = request.GET.get('oid', None)
    if request.method == 'POST':
        form = AddSoftwareForm(request.POST)
        if form.is_valid():
            new_software = Software(title=form.cleaned_data['title'],
                                    authors=form.cleaned_data['authors'],
                                    description=form.cleaned_data['description'],
                                    project_url=form.cleaned_data['project_url'],
                                    pub_date=datetime.datetime.now(),
                                    updated_date=datetime.datetime.now(),
                                    tags=form.cleaned_data['tags'],
                                    language=form.cleaned_data['language'],
                                    os_license=form.cleaned_data['os_license'],
                                    tarball=form.cleaned_data['tarball'],
                                    )
            if original_id:
                new_software.original_id = original_id
            save_tarball(new_software)
            new_software.save()
            return HttpResponseRedirect(new_software.get_absolute_url())
        else:
            print form
    else:
        form = AddSoftwareForm()
    return render_to_response('software_add.html',
                              { 'form': form },
                              context_instance=RequestContext(request))

def update_software(request, software_id):
    """
    Detail view of a Software.
    
    Context::
        object
            The Software object.
    
    Template::
        software_detail.html
    
    """
    entry = get_object_or_404(Software, pk=software_id)

    if not request.user.is_authenticated():
       return HttpResponseRedirect('/accounts/login?next=%s' % request.path)

    return update_object(request, Software, software_id, template_name='software_add.html')
