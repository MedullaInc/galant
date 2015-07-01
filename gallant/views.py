from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from gallant.forms import *


class ClientCreate(CreateView):
    form_class = ClientForm
    template_name = "gallant/client_form.html"

    def form_valid(self, form):
        obj = form.save(commit=True)
        user = GallantUser.objects.get(id=self.request.user.id)
        note = Note.objects.create(text=form.cleaned_data['notes'], created_by=user)
        obj.notes.add(note)
        obj.save()
        return HttpResponseRedirect(self.get_success_url())