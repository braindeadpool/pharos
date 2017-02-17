from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import floppyforms

from bootcamp.settings import ALLOWED_SIGNUP_DOMAINS
from .models import Profile
import bootcamp.core.all_users as all_users


def SignupDomainValidator(value):
    if '*' not in ALLOWED_SIGNUP_DOMAINS:
        try:
            domain = value[value.index("@"):]
            if domain not in ALLOWED_SIGNUP_DOMAINS:
                raise ValidationError('Invalid domain. Allowed domains on this network: {0}'.format(
                    ','.join(ALLOWED_SIGNUP_DOMAINS)))  # noqa: E501

        except Exception:
            raise ValidationError('Invalid domain. Allowed domains on this network: {0}'.format(
                ','.join(ALLOWED_SIGNUP_DOMAINS)))  # noqa: E501


def ForbiddenUsernamesValidator(value):
    forbidden_usernames = ['admin', 'settings', 'news', 'about', 'help',
                           'signin', 'signup', 'signout', 'terms', 'privacy',
                           'cookie', 'new', 'login', 'logout', 'administrator',
                           'join', 'account', 'username', 'root', 'blog',
                           'user', 'users', 'billing', 'subscribe', 'reviews',
                           'review', 'blog', 'blogs', 'edit', 'mail', 'email',
                           'home', 'job', 'jobs', 'contribute', 'newsletter',
                           'shop', 'profile', 'register', 'auth', 'labs'
                                                                  'authentication', 'campaign', 'config', 'delete',
                           'remove', 'forum', 'forums', 'download',
                           'downloads', 'contact', 'blogs', 'feed', 'feeds',
                           'faq', 'intranet', 'log', 'registration', 'search',
                           'explore', 'rss', 'support', 'status', 'static',
                           'media', 'setting', 'css', 'js', 'follow',
                           'activity', 'questions', 'projects', 'network', 'labmanager']

    if value.lower() in forbidden_usernames:
        raise ValidationError('This is a reserved word.')


def InvalidUsernameValidator(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('Enter a valid username.')


def UniqueEmailValidator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this Email already exists.')


def UniqueUsernameIgnoreCaseValidator(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('User with this Username already exists.')


class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        label="First Name*",
        required=True)

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        label="Last Name*",
        required=True)

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True,
        label="Set Username*",
        help_text='Usernames may contain <strong>alphanumeric</strong>, <strong>_</strong> and <strong>.</strong> characters<br/>You will use this username to login into this portal')  # noqa: E261

    # identification = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     max_length=50,
    #     required=True,
    #     label="ID*",
    #     help_text="User ID alloted to this user"
    # )

    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True,
        label="Email*",
        max_length=75)

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Set Password*",
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm your password*",
        required=True)

    role = forms.CharField(
        widget=forms.Select(choices=[('User', 'User'), ('Lab Manager', 'Lab Manager')]),
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

    picture = forms.ImageField(
        required=False,
        label='Profile Picture',
    )

    web_page = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=75,
        label="Home Page / Personal web page",
        required=False)

    institution = forms.CharField(
        widget=floppyforms.widgets.Input(
            datalist=sorted(set([x.profile.institution for x in User.objects.filter(is_active=True)])),
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

    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=200,
        label="Biography",
        required=False)

    class Meta:
        model = User
        exclude = ['last_login', 'date_joined']
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password', 'role', 'job_title',
                  'picture', 'web_page', 'institution', 'city', 'state', 'country', 'bio']

    def __init__(self, *args, **kwargs):
        datalists = kwargs.pop('datalists', None)

        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(ForbiddenUsernamesValidator)
        self.fields['username'].validators.append(InvalidUsernameValidator)
        self.fields['username'].validators.append(
            UniqueUsernameIgnoreCaseValidator)
        self.fields['email'].validators.append(UniqueEmailValidator)
        self.fields['email'].validators.append(SignupDomainValidator)

        # pass the datalist items onto floppyform widgets
        # if datalists is not None:
        #     for field in datalists:
        #         print field, datalists[field]
        #         self.fields[field].widget = floppyforms.widgets.Input(datalist=datalists[field],
        #                                                               attrs={'class': 'form-control'}),

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class(
                ['Passwords don\'t match'])
        return self.cleaned_data
