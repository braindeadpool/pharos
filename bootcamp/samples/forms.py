from django import forms

from bootcamp.samples.models import Sample
from django.contrib.auth.models import User
import bootcamp.core.all_users as all_users
from bootcamp.samples.models import Material


class SampleForm(forms.ModelForm):
    # materials = Material.objects.all()
    materials = []
    category_list = set()
    material_name = set()
    for each in materials:
        category_list.add(each.category)
        material_name.add(each.name)
    category_list = list(sorted(category_list))
    material_name = list(sorted(material_name))

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
    print "printing users in form"
    all_users.update()
    users = all_users.getUserTuple()
    print users

    collaborators = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                              choices=users, required=True)

    class Meta:
        model = Sample
        fields = ['title', 'description', 'tags', 'status', 'collaborators']
