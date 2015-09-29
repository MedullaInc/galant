from itertools import chain
from django import forms
from django.conf import settings
from django.db.models import Count
from django.utils.translation import get_language
from gallant import models as g
from quotes import models as q
from djangular.forms import NgModelForm, NgFormValidationMixin
from djangular.styling.bootstrap3.forms import Bootstrap3ModelForm


class GallantNgModelForm(NgModelForm, Bootstrap3ModelForm, NgFormValidationMixin):
    pass


class UserModelForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserModelForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.user = self.user
        return super(UserModelForm, self).save(*args, **kwargs)


class UserModelNgForm(GallantNgModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserModelNgForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.user = self.user
        return super(UserModelNgForm, self).save(*args, **kwargs)


class ClientForm(UserModelNgForm):
    class Meta:
        model = g.Client
        fields = ['name', 'email', 'type', 'size', 'status', 'language', 'currency']

    def __init__(self, *args, **kwargs):
        kwargs.update(prefix='client')
        super(ClientForm, self).__init__(*args, **kwargs)
        self.initial['language'] = get_language()


class ServiceForm(UserModelForm):
    class Meta:
        model = g.Service
        fields = ['name', 'description', 'cost', 'quantity', 'type']

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['notes'] = forms.CharField(
            widget=forms.Textarea(attrs={'rows': 5}), required=False)


class ServiceOnlyForm(UserModelForm):
    class Meta:
        model = g.Service
        fields = ['name', 'description', 'cost', 'quantity', 'type']


class NoteForm(UserModelNgForm):
    class Meta:
        model = g.Note
        fields = ['text']

    def __init__(self, *args, **kwargs):
        kwargs.update(prefix='note')
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget = forms.Textarea(attrs={'rows': 3})
        self.fields['text'].label = 'Notes'
        self.fields['text'].help_text = ''


class ProjectForm(UserModelForm):

    class Meta:
        model = g.Project
        fields = ['name', 'status']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['notes'] = forms.CharField(
            widget=forms.Textarea(attrs={'rows': 5}), required=False)


class ProjectOnlyForm(UserModelForm):

    class Meta:
        model = g.Project
        fields = ['name', 'status']

    def __init__(self, *args, **kwargs):
        super(ProjectOnlyForm, self).__init__(*args, **kwargs)

        if self.instance.id is not None:
            quote_set_a = self.instance.quote_set.all_for(self.user, 'view_quote')
            quote_set_b = []

            if len(quote_set_a) > 0:
                client = quote_set_a[0].client
                quote_set_b = q.Quote.objects.all_for(
                    self.user, 'view_quote').annotate(projects_count=Count('projects')).filter(
                    projects_count=0, status=5, client_id=client.id)

            linked_quotes = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple({'checked': True}),
                                                           queryset=quote_set_a)

            available_quotes = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple({'checked': False}),
                                                              queryset=quote_set_b, required=False)

            if len(linked_quotes.queryset) > 0:
                self.fields['linked_quotes'] = linked_quotes

            if len(available_quotes.queryset) > 0:
                self.fields['available_quotes'] = available_quotes


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

    def __init__(self, request, app_title, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.request = request

        self.fields['feedback'].label = 'Current section: %s' % app_title
        if request.user.is_authenticated():
            self.initial['email'] = request.user.email
            self.fields['email'].widget = forms.HiddenInput()


class CreateUserForm(forms.Form):
    email = forms.EmailField(help_text='Enter new user\'s email. A registration link will be sent.')


class GallantUserForm(forms.ModelForm):
    class Meta:
        model = g.GallantUser
        fields = ['name', 'company_name']


class ContactInfoForm(GallantNgModelForm):
    class Meta:
        model = g.ContactInfo
        fields = ['phone_number', 'country', 'address', 'address_2',
                  'city', 'state', 'zip']

    def __init__(self, *args, **kwargs):
        kwargs.update(prefix='contact_info')
        super(ContactInfoForm, self).__init__(*args, **kwargs)


class EmailForm(forms.Form):
    email = forms.EmailField()

