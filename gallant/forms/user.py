from django import forms
from djangular.forms import NgModelForm, NgFormValidationMixin
from djangular.styling.bootstrap3.forms import Bootstrap3ModelForm
from django.conf import settings
from django.utils.translation import get_language
from gallant import models as g


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

