from django import forms

from bootcamp.samples.models import Sample
import bootcamp.core.all_users as all_users
import bootcamp.devices.all_devices as all_devices
from bootcamp.projects.models import Project


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['name', 'identification', 'description', 'tags', 'project']

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

    # devicelist = all_devices.getDeviceTuple()
    # devices = forms.ChoiceField(
    #     widget=forms.RadioSelect(),
    #     choices=devicelist, label='Sample Device', required=True
    # )

    def __init__(self, *args, **kwargs):
        user = None
        if kwargs is not None:
            user = kwargs.pop('user', None)
        super(SampleForm, self).__init__(*args, **kwargs)
        if user:
            projects = Project.objects.filter(create_user=user)
            label = 'No Project'
            if len(projects) == 0:
                label = 'This user has no project'
            self.fields['project'] = forms.ModelChoiceField(widget=forms.RadioSelect(),
                                                            queryset=projects,
                                                            empty_label=label,
                                                            to_field_name='title')
