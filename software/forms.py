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

def addsoftware(request):
    """
    Show the software form, and capture the information
    """

    def save_tarball(object):
        """
        Retrieve filename and save the file
        """
        if request.FILES.has_key('tarball'):
            filename = request.FILES['tarball']['filename']
            object.save_tarball_file(filename, request.FILES['tarball']['content'])

    if not request.user.is_authenticated():
       return HttpResponseRedirect('/accounts/login?next=%s' % request.path)

    AddSoftwareForm = forms.form_for_model(Software)

    #,initial=request.user.__str__(),initial='http://'
    original_id = request.GET.get('oid', None)
    if request.method == 'POST':
        form = AddSoftwareForm(request.POST)
        if form.is_valid():
            new_software = Software(title=form.cleaned_data['title'],
                                    authors=form.cleaned_data['authors'],
                                    contact=form.cleaned_data['authors'],
                                    description=form.cleaned_data['description'],
                                    project_url=form.cleaned_data['project_url'],
                                    tags=form.cleaned_data['tags'],
                                    language=form.cleaned_data['language'],
                                    os_license=form.cleaned_data['os_license'],
                                    pub_date=datetime.datetime.now(),
                                    updated_date=datetime.datetime.now(),
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
    return render_to_response('software/software_add.html',
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
    if not request.user.is_authenticated():
       return HttpResponseRedirect('/accounts/login?next=%s' % request.path)

    return update_object(request, Software, software_id, login_required=True, template_name='software/software_add.html')
