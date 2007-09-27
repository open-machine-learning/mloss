"""
Forms for adding Software

"""
import datetime
from django import newforms as forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from models import Software


class AddSoftwareForm(forms.Form):
    """
    Form used for adding Software
    
    """
    title = forms.CharField(widget=forms.TextInput(attrs={'size':80}))
    authors = forms.CharField(widget=forms.TextInput(attrs={'size':80}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':20,'cols':80}))
    project_url = forms.URLField(widget=forms.TextInput(attrs={'size':80})) 


def addsoftware(request):
    """
    Show the software form, and capture the information
    """
    original_id = request.GET.get('oid', None)
    if request.method == 'POST':
        form = AddSoftwareForm(request.POST)
        if form.is_valid():
            form.full_clean()
            new_software = Software(title=form.cleaned_data['title'],
                                   # somehow django is unhappy
                                   #authors=form.cleaned_data['authors'],
                                   description=form.cleaned_data['description'],
                                   project_url=form.cleaned_data['project_url'],
                                   pub_date=datetime.datetime.now(),
                                   updated_date=datetime.datetime.now(),
                                   )
            if original_id:
                new_software.original_id = original_id
            new_software.save()
            return HttpResponseRedirect(new_software.get_absolute_url())
        else:
            print form
    else:
        form = AddSoftwareForm()
    return render_to_response('software_add.html',
                              { 'form': form },
                              context_instance=RequestContext(request))
#addsoftware = login_required(addsoftware)
