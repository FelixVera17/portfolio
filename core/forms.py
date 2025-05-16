from django.forms import forms
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label='')
    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs['class']  = 'form-control'
        self.fields['file'].widget.attrs['style'] = 'width: 85%; float:left'