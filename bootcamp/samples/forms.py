from django import forms

from bootcamp.samples.models import Sample
import bootcamp.core.all_users as all_users
import bootcamp.devices.all_devices as all_devices


class SampleForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    identification = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=4000)
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255, required=False,
        help_text='Use spaces to separate the tags, such as "java jsf primefaces"')
    devicelist = all_devices.getDeviceTuple()
    devices = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        choices=devicelist, label='Sample Devices', required=True
    )
    users = all_users.getUserTuple()
    collaborators = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                              choices=users, label='Sample Users', required=True)

    class Meta:
        model = Sample
        fields = ['name', 'identification', 'description', 'tags', 'collaborators']
