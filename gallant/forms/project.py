from django import forms
from django.db.models import Count
from gallant import models as g
from quotes import models as q
from user import UserModelForm


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
