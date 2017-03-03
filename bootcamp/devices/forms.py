from django import forms

from bootcamp.devices.models import Device
from django.contrib.auth.models import User
from django.conf import settings
import bootcamp.core.all_users as all_users
from bootcamp.devices.models import Device
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from multiupload.fields import MultiImageField


class DeviceForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    identification = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    description = forms.CharField(
        widget=SummernoteWidget(),
        max_length=4000)
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255, required=False,
        help_text='Use spaces to separate the tags, such as "java jsf primefaces"')
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    pictures = MultiImageField(min_num=1, max_num=10, max_file_size=1024*1024*5, required=False)

    users = all_users.getUserTuple()
    collaborators = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                              choices=users, label='Device Users', required=True)

    class Meta:
        model = Device
        fields = ['name', 'identification', 'description', 'pictures', 'tags', 'location', 'collaborators']
