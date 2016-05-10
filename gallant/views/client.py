from itertools import chain
import json
from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse
from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from gallant import forms, serializers
from gallant import models as g
from briefs import models as b
from gallant.utils import get_one_or_404, GallantObjectPermissions, GallantViewSetPermissions, get_field_choices
from django.utils.translation import ugettext_lazy as _
from gallant.views.user import UserModelViewSet
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import permission_classes


class ClientList(View):
    def get(self, request):
        request.breadcrumbs(_('Clients'), request.path_info)
        return TemplateResponse(request=request,
                                template="gallant/client_list.html",
                                context={'title': 'Clients',
                                         'object_list': g.Client.objects.all_for(request.user)})


class ClientUpdate(View):
    def get(self, request, **kwargs):
        self.object = get_one_or_404(request.user, 'change_client', g.Client, pk=kwargs['pk'])
        form = forms.ClientForm(request.user, instance=self.object)
        return self.render_to_response({'object': self.object, 'form': form,
                                        'contact_form': forms.ContactInfoForm(request.user,
                                            instance=self.object.contact_info),
                                        'note_form': forms.NoteForm(request.user)})

    def post(self, request, **kwargs):
        if 'pk' in kwargs:
            self.object = get_one_or_404(request.user, 'change_client', g.Client, pk=kwargs['pk'])
        else:
            # No perms currently needed to create
            self.object = None

        form = forms.ClientForm(request.user, request.POST, instance=self.object)
        contact_form = forms.ContactInfoForm(request.user, request.POST,
                                             instance=getattr(self.object, 'contact_info', None))
        note_form = forms.NoteForm(request.user, request.POST)

        if form.is_valid() and contact_form.is_valid():
            return self.form_valid(form, contact_form, note_form)
        else:
            response = {'status': 0, 'errors': list(chain(form.errors.items(), contact_form.errors.items()))}
            return HttpResponse(json.dumps(response), content_type='application/json')

    def render_to_response(self, context):
        context.update({'title': 'Edit Client'})

        self.request.breadcrumbs(_('Clients'), reverse('clients'))
        if self.object:
            self.request.breadcrumbs([(_(self.object.name), reverse('client_detail', args=[self.object.id])),
                                      (_('Edit'), self.request.path_info)])
        else:
            self.request.breadcrumbs(_('Add'), self.request.path_info)
        return TemplateResponse(request=self.request,
                                template="gallant/client_form.html",
                                context=context)

    def form_valid(self, form, contact_form, note_form):
        obj = form.save(commit=True)
        if note_form.is_valid():
            note = note_form.save()
        else:
            note = g.Note.objects.create(user=obj.user)
        note.text = '[Updated]\n' + note.text
        note.save()
        obj.notes.add(note)
        obj.contact_info = contact_form.save()
        obj.currency = obj.user.currency
        obj.save()
        messages.success(self.request, 'Client saved.')
        response = {'status': 0, 'redirect': reverse('client_detail', args=[obj.id])}
        return HttpResponse(json.dumps(response), content_type='application/json')


class ClientCreate(ClientUpdate):
    def get(self, request):
        self.object = None
        request.breadcrumbs([(_('Clients'), reverse('clients')),
                             (_('Add'), request.path_info)])
        form = forms.ClientForm(request.user)
        context = {'form': form,
                   'contact_form': forms.ContactInfoForm(request.user),
                   'title': 'Add Client'}
        return TemplateResponse(request=self.request,
                                template="gallant/client_form.html",
                                context=context)


def client_detail(request, pk):
    client = get_one_or_404(request.user, 'view_client', g.Client, pk=pk)

    if request.method == 'POST' and request.user.has_perm('change_client', client):
        form = forms.NoteForm(request.user, request.POST)
        if form.is_valid():
            note = g.Note.objects.create(text=form.cleaned_data['text'], user=request.user)
            client.notes.add(note)
            client.save()
            return HttpResponseRedirect(reverse('client_detail', args=[client.id]))
    else:
        form = forms.NoteForm(request.user)  # An unbound form

    request.breadcrumbs([(_('Clients'), reverse('clients')),
                         (_(client.name), reverse('client_detail', args=[client.id]))])

    return TemplateResponse(request=request,
                            template="gallant/client_detail.html",
                            context={'object': client, 'form': form,
                                     'template_list': b.BriefTemplate.objects
                                                       .all_for(request.user),'title': client.name })


def client_work_detail(request, pk):
    client = get_one_or_404(request.user, 'view_client', g.Client, pk=pk)

    # TODO: add filter_for to usermodelmanager
    projects = g.Project.objects.all_for(request.user).filter(quote__client=client)

    request.breadcrumbs([(_('Clients'), reverse('clients')),
                         (_(client.name), reverse('client_detail', args=[client.id]))])

    return TemplateResponse(request=request,
                            template="gallant/client_work_detail.html",
                            context={'object': client,
                                     'template_list': b.BriefTemplate.objects
                                                       .all_for(request.user),'title': client.name,'projects': projects })


def client_money_detail(request, pk):
    client = get_one_or_404(request.user, 'view_client', g.Client, pk=pk)

    request.breadcrumbs([(_('Clients'), reverse('clients')),
                         (_(client.name), reverse('client_detail', args=[client.id]))])

    return TemplateResponse(request=request,
                            template="gallant/client_money_detail.html",
                            context={'object': client,
                                     'template_list': b.BriefTemplate.objects
                                                       .all_for(request.user), 'title': client.name})


class ClientDelete(View):
    def get(self, request, **kwargs):
        client = get_one_or_404(request.user, 'change_client', g.Client, id=kwargs['pk'])
        client.soft_delete()

        return HttpResponseRedirect(reverse('clients'))


class ClientDetailAPI(generics.RetrieveUpdateAPIView):
    model = g.Client
    serializer_class = serializers.ClientSerializer
    permission_classes = [
        GallantObjectPermissions
    ]

    def get_queryset(self):
        return self.model.objects.all_for(self.request.user)


def client_fields_json(request):
    return JsonResponse(get_field_choices(g.Client), safe=False)


class ClientsAPI(ModelViewSet):
    model = g.Client
    serializer_class = serializers.ClientSerializer
    permission_classes = [
        GallantViewSetPermissions
    ]

    def get_queryset(self):
        user = self.request.GET.get('user', None)
        if user:
            return self.model.objects.all_for(self.request.user).filter(user_id=user)
        else:
            return self.model.objects.all_for(self.request.user)
