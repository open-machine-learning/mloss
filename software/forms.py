"""
Forms for adding Software

"""
import datetime
from django import newforms as forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from models import Software


#class AddSoftwareForm(forms.Form):
#    """
#    Form used for adding Software
#    
#    """
#    title = forms.CharField(widget=forms.TextInput(attrs={'size':80}))
#    #authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all())
#    authors = forms.CharField(widget=forms.TextInput(attrs={'size':80}))
#    description = forms.CharField(widget=forms.Textarea(attrs={'rows':20,'cols':80}))
#    project_url = forms.URLField(widget=forms.TextInput(attrs={'size':80})) 
#    keyword1 = forms.CharField(widget=forms.TextInput(attrs={'size':80}),required=False)
#    keyword2 = forms.CharField(widget=forms.TextInput(attrs={'size':80}),required=False)
#    keyword3 = forms.CharField(widget=forms.TextInput(attrs={'size':80}),required=False)
#    keyword4 = forms.CharField(widget=forms.TextInput(attrs={'size':80}),required=False)
#    keyword5 = forms.CharField(widget=forms.TextInput(attrs={'size':80}),required=False)
#    language = forms.CharField(widget=forms.TextInput(attrs={'size':80}),required=False)
#    os_license = forms.CharField(widget=forms.TextInput(attrs={'size':80}),required=False)
#    tarball = forms.FileField(widget=forms.FileInput, required=False)

AddSoftwareForm = forms.form_for_model(Software)



  
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
            #filename = object.user.username + '_' + filename
            object.save_tarball_file(filename, request.FILES['tarball']['content'])

    
    original_id = request.GET.get('oid', None)
    if request.method == 'POST':
        #post_data = request.POST.copy()
        #post_data.update(request.FILES)
        form = AddSoftwareForm(request.POST)
        if form.is_valid():
            # somehow the default behaviour doesn't work with file uploads
            #new_software = Software(form)
            new_software = Software(title=form.cleaned_data['title'],
                                    authors=form.cleaned_data['authors'],
                                    description=form.cleaned_data['description'],
                                    project_url=form.cleaned_data['project_url'],
                                    pub_date=datetime.datetime.now(),
                                    updated_date=datetime.datetime.now(),
                                    keyword1=form.cleaned_data['keyword1'],
                                    keyword2=form.cleaned_data['keyword2'],
                                    keyword3=form.cleaned_data['keyword3'],
                                    keyword4=form.cleaned_data['keyword4'],
                                    keyword5=form.cleaned_data['keyword5'],
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
#addsoftware = login_required(addsoftware)
