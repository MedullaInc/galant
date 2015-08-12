from django import forms
from django.conf import settings
from django.utils.translation import get_language
from gallant import models as g


class UserModelForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserModelForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.user = self.user
        return super(UserModelForm, self).save(*args, **kwargs)


class ClientForm(UserModelForm):
    class Meta:
        model = g.Client
        fields = ['name', 'type', 'size', 'status', 'language', 'currency']

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.initial['language'] = get_language()
        self.fields['notes'] = forms.CharField(
            widget=forms.Textarea(attrs={'rows': 5}), required=False)


class ServiceForm(UserModelForm):
    class Meta:
        model = g.Service
        fields = ['name', 'description', 'cost', 'quantity', 'type']

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['notes'] = forms.CharField(
            widget=forms.Textarea(attrs={'rows': 5}), required=False)


class NoteForm(UserModelForm):
    class Meta:
        model = g.Note
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['text'] = forms.CharField(
            widget=forms.Textarea(attrs={'rows': 3}))


class ProjectForm(UserModelForm):

    class Meta:
        model = g.Project
        fields = ['name', 'status']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['notes'] = forms.CharField(
            widget=forms.Textarea(attrs={'rows': 5}), required=False)


class LanguageForm(forms.Form):
    language = forms.ChoiceField(choices=settings.LANGUAGES, label='', initial=get_language())


class SignUpRequestForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    company = forms.CharField(max_length=255, help_text='Enter company name or "self-employed"')
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5}),
                                  max_length=2000, help_text='Tell us about yourself (optional)')


class FeedbackForm(forms.Form):
    email = forms.EmailField()
    feedback = forms.CharField(required=False,
                               widget=forms.Textarea(attrs={'rows': 10}),
                               max_length=2000,
                               help_text='Please enter comments, thoughts, or bug reports.')

    def __init__(self, request, section_title, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.request = request

        self.fields['feedback'].label = 'Current section: %s' % section_title
        if request.user.is_authenticated():
            self.initial['email'] = request.user.email
            self.fields['email'].widget = forms.HiddenInput()


class CreateUserForm(forms.Form):
    email = forms.EmailField(help_text='Enter new user\'s email. A registration link will be sent.')


class GallantUserForm(forms.ModelForm):
    class Meta:
        model = g.GallantUser
        fields = ['name', 'company_name']


class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = g.ContactInfo
        fields = ['phone_number', 'country', 'address', 'address_2',
                  'city', 'state', 'zip']


class EmailForm(forms.Form):
    email = forms.EmailField()

