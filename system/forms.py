# forms.py 
from django import forms 
from .models import *
  
class HeaderForm(forms.ModelForm): 
  
    class Meta: 
        model = Header
        fields = ['img'] 

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ('description', 'document', )


class UploadFileForm(forms.Form):
    file = forms.FileField()