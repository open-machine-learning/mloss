"""
Forms for adding Software

"""

from django import newforms as forms

# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary.
attrs_dict = { 'class': 'required' }

class AddSoftwareForm(forms.Form):
    """
    Form used for adding Software
    
    """
    def __init__(self, *args, **kwargs):
        super(AddSoftwareForm, self).__init__(*args, **kwargs)
    
    title = forms.CharField(max_length=250, widget=forms.TextInput(attrs=attrs_dict))
    description = forms.CharField(widget=forms.Textarea(attrs=attrs_dict))
    project_url = forms.URLField(widget=forms.Textarea(attrs=attrs_dict))


