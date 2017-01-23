from django import forms
from django.contrib.auth.models import User
import floppyforms
from bootcamp.authentication.models import Profile
import bootcamp.core.all_users as all_users


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        max_length=50,
        label="First Name*",
        required=True)
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        max_length=50,
        label="Last Name*",
        required=True)
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True,
        label="Email*",
        max_length=75)

    role = forms.CharField(
        widget=forms.Select(attrs={"disabled": 'true'}, choices=[('User', 'User'), ('Lab Manager', 'Lab Manager')]),
        required=True,
        label="Role*",
        max_length=75)

    job_title = forms.CharField(
        widget=forms.Select(
            choices=[('Student', 'Student'), ('Staff', 'Staff'), ('Professor', 'Professor'), ('Visitor', 'Visitor'),
                     ('Industry', 'Industry')]),
        required=True,
        label="Job Title*",
        max_length=75)

    web_page = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=75,
        label="Home Page",
        required=False)

    institution = forms.CharField(
        widget=floppyforms.widgets.Input(
            #datalist=sorted(set([x.profile.institution for x in User.objects.filter(is_active=True)])),
            attrs={'class': 'form-control'}),
        max_length=100,
        label="Affliated Institution*",
        required=True)

    #     states = []
    #     countries = []
    #     all_users.update()
    #     all_data = all_users.getUserList()
    #     countries = sorted(set([x.profile.country for x in all_data]))
    #     states = sorted(set([x.profile.state for x in all_data]))
    #     print all_data
    #     print "Countries"
    #     print countries
    #     print "States"
    #     print states
    #    [x.profile.state for x in User.objects.filter(is_active=True).order_by('profile.state')]

    city = forms.CharField(
        widget=floppyforms.widgets.Input(
            #datalist=sorted(set([x.profile.city for x in User.objects.filter(is_active=True)])),
            attrs={'class': 'form-control'}),
        max_length=75,
        label="City*",
        required=True)

    state = forms.CharField(
        widget=floppyforms.widgets.Input(
            #datalist=sorted(set([x.profile.state for x in User.objects.filter(is_active=True)])),
            attrs={'class': 'form-control'}),
        max_length=75,
        label="State*",
        required=True)

    country = forms.CharField(
        widget=floppyforms.widgets.Input(
            #datalist=sorted(set([x.profile.country for x in User.objects.filter(is_active=True)])),
            attrs={'class': 'form-control'}),
        max_length=75,
        label="Country*",
        required=True)

    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=200,
        label="Tell us about yourself",
        required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role', 'job_title',
                  'web_page', 'institution', 'city', 'state', 'country', 'bio']


class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Old password",
        required=True)

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New password",
        required=True)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm new password",
        required=True)

    class Meta:
        model = User
        fields = ['id', 'old_password', 'new_password', 'confirm_password']

    def clean(self):
        super(ChangePasswordForm, self).clean()
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        id = self.cleaned_data.get('id')
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] = self.error_class([
                'Old password don\'t match'])
        if new_password and new_password != confirm_password:
            self._errors['new_password'] = self.error_class([
                'Passwords don\'t match'])
        return self.cleaned_data
