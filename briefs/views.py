from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from briefs import forms
from briefs import models

# Create your views here.
def index(request):

    form = forms.TestForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form1 = form.save(commit=False)
            form1.save()
            return HttpResponseRedirect(reverse('briefs'))

    return render(request, 'briefs/index.html', {
        'form': form,
    })