from django import forms
from django.contrib.auth.models import User
from bootcamp.labs.models import Lab
import floppyforms


# To add new labs, can only be accessed by lab manager
class LabForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=4000)
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255, required=False,
        help_text='Use spaces to separate the tags, such as "java jsf primefaces"')  # noqa: E501

    building = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)

    institution = forms.CharField(
        widget=floppyforms.widgets.Input(
            datalist=sorted(set([x.profile.institution for x in User.objects.filter(is_active=True)])),
            attrs={'class': 'form-control'}),
        max_length=100,
        label="Institution*",
        required=True)

    city = forms.CharField(
        widget=floppyforms.widgets.Input(
            datalist=sorted(set([x.profile.city for x in User.objects.filter(is_active=True)])),
            attrs={'class': 'form-control'}),
        max_length=75,
        label="City*",
        required=True)

    state = forms.CharField(
        widget=floppyforms.widgets.Input(
            datalist=sorted(set([x.profile.state for x in User.objects.filter(is_active=True)])),
            attrs={'class': 'form-control'}),
        max_length=75,
        label="State*",
        required=True)

    country = forms.CharField(
        widget=floppyforms.widgets.Input(
            datalist=sorted(set([x.profile.country for x in User.objects.filter(is_active=True)])),
            attrs={'class': 'form-control'}),
        max_length=75,
        label="Country*",
        required=True)

    class Meta:
        model = Lab
        fields = ['name', 'description', 'tags', 'status', 'building', 'institution', 'city', 'state', 'country']
