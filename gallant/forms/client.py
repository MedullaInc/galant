from django.utils.translation import get_language
from gallant import models as g
from user import UserModelNgForm


class ClientForm(UserModelNgForm):
    class Meta:
        model = g.Client
        fields = ['name', 'email', 'company',
                  'status', 'language', 'referred_by']

    def __init__(self, *args, **kwargs):
        kwargs.update(prefix='client')
        super(ClientForm, self).__init__(*args, **kwargs)
        self.initial['language'] = get_language()