from django.views.generic.edit import CreateView
from gallant.forms import *


class ClientCreate(CreateView):
    form_class = ClientForm
    template_name = "gallant/client_form.html"