from allauth.account.forms import SetPasswordForm
from django import forms
from django.contrib.auth import password_validation
from djng.forms import NgModelForm, NgFormValidationMixin
from djng.styling.bootstrap3.forms import Bootstrap3ModelForm
from django.conf import settings
from django.utils.translation import get_language
from django.utils.translation import ugettext, ugettext_lazy as _
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
    name = forms.CharField(max_length=255, required=False)
    email = forms.EmailField()
    company = forms.CharField(max_length=255, required=False, help_text='Enter company name or "self-employed"')
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
    required_css_class = 'required'
    class Meta:
        model = g.GallantUser
        fields = ['name', 'company_name', 'currency', 'phone_number', 'country', 'address', 'address_2',
                  'city', 'state', 'zip']


class GallantSetPasswordForm(forms.Form):
    required_css_class = 'required'
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput,
                                    help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(GallantSetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class ContactInfoForm(UserModelNgForm):
    class Meta:
        model = g.ContactInfo
        fields = ['phone_number', 'country', 'address', 'address_2',
                  'city', 'state', 'zip']

    def __init__(self, user, *args, **kwargs):
        kwargs.update(prefix='contact_info')
        super(ContactInfoForm, self).__init__(user, *args, **kwargs)


class EmailForm(forms.Form):
    email = forms.EmailField()

