# records/forms.py

from django import forms
from .models import Document
from .models import UserRecord

class RecordForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'pdf_file']

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserRecord
        fields = ['email', 'password', 'role']









