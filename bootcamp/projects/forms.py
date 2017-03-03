from django import forms

from bootcamp.projects.models import Project
from django.contrib.auth.models import User
import bootcamp.core.all_users as all_users
from bootcamp.projects.models import Material, Device, Sample


class ProjectForm(forms.ModelForm):
    materials = Material.objects.all()
    devices = Device.objects.all()
    # samples = Sample.objects.all()

    # materials = []
    devices = []
    samples = []
    category_list = set()
    material_name = set()
    device_name = set()
    for each in materials:
        category_list.add(each.category)
        material_name.add(each.name)
    for each in devices:
        device_name.add(each.name)
    category_list = list(sorted(category_list))
    material_name = list(sorted(material_name))
    device_name = list(sorted(device_name))

    status = forms.CharField(widget=forms.HiddenInput())
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=4000)
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255, required=False,
        help_text='Use spaces to separate the tags, such as "java jsf primefaces"')  # noqa: E501

    all_users.update()
    users = all_users.getUserTuple()

    collaborators = forms.MultipleChoiceField(widget=forms.HiddenInput(),
                                              choices=users, required=False)

    class Meta:
        model = Project
        fields = ['title', 'description', 'tags', 'status', 'collaborators']


class SearchForm(forms.Form):
    title = forms.CharField(max_length=255, required=False)
    author = forms.CharField(max_length=255, required=False)
    daterange = forms.CharField(label='Dates', required=False)
    tags = forms.CharField(max_length=255, required=False)
