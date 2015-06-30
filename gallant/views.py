from django.views.generic.edit import CreateView, UpdateView, DeleteView
from gallant.models import *


class ClientCreate(CreateView):
    model = Client
    fields = ["name", "type", "size", "status", "language", "currency", "notes"]