from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.db.models import Q
from .models import Contact
from .forms import ContactForm, SearchForm, ImportForm
from django.views.generic import View, ListView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
import json
from django.db import IntegrityError
from django.core.exceptions import ValidationError


def html_parser():
    # Html parser
    worth_list = []
    url = 'http://breffi.ru/ru/about'
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    worth = soup.find('div', {'class': 'content-section worth'})
    items = worth.find_all('div', {'class': 'content-section__itemtitle'})
    for item in items:
        worth_list.append(item.text)
    return worth_list


class Contacts(ListView):
    template_name = 'index.html'
    form_class = SearchForm
    context_object_name = 'contacts'
    paginate_by = 10

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            return Contact.objects.filter(
                Q(name__icontains=query) | Q(company__icontains=query)
            )
        return Contact.objects.all()

    def get_context_data(self, **kwargs):
        context = super(Contacts, self).get_context_data(**kwargs)
        context['page_title'] = 'Контакты'
        context['worth_list'] = html_parser()
        context['form'] = self.form_class(self.request.GET)
        return context


class ContactNew(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact_new.html'


class ContactDetail(DetailView):
    model = Contact
    template_name = 'contact_detail.html'
    context_object_name = 'contact'

    def get_context_data(self, **kwargs):
        context = super(ContactDetail, self).get_context_data(**kwargs)
        context['page_title'] = self.get_object().name
        return context


class ContactEdit(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact_edit.html'


class ContactDelete(SuccessMessageMixin, DeleteView):
    model = Contact
    template_name = 'contact_delete.html'
    success_url = reverse_lazy('contacts_list')
    success_message = "Запись удалена"


class ExportData(View):

    def get(self, request, *args, **kwargs):
        data = json.dumps(
            list(Contact.objects.values(
                'name', 'company', 'email', 'phone', 'interest')),
            ensure_ascii=False
        )
        response = HttpResponse(data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="export.json"'
        return response
        # return self.render_to_json(data)


# class ImportFromJSONMixin(object):

#     def validate_instance(self, data, form):
#         contact = Contact(
#             name=data['name'],
#             company=data['company'],
#             email=data['email'],
#             phone=data['phone'],
#             interest=data['interest'],
#         )
#         try:
#             contact.full_clean()
#         except ValidationError as e:
#             messages.error(self.request, e)
#             return self.form_invalid(form)
#         return contact


class ImportData(SuccessMessageMixin, FormView):
    form_class = ImportForm
    template_name = 'import_form.html'
    success_url = reverse_lazy('contacts_list')
    success_message = "Импорт прошел успешно"

    def form_valid(self, form):
        file = form.cleaned_data['file']
        try:
            data = json.loads(file.read().decode('utf8'))
        except:
            messages.error(self.request, "Формат данных некорректен")
            return self.form_invalid(form)

        items = []
        for item in data:
            contact = Contact(
                name=item['name'],
                company=item['company'],
                email=item['email'],
                phone=item['phone'],
                interest=item['interest'],
            )

            try:
                contact.full_clean()
            except ValidationError as e:
                messages.error(self.request, e)
                return self.form_invalid(form)

            items.append(contact)

        Contact.objects.bulk_create(items)
        # try:
        #     Contact.objects.bulk_create(items)
        # except IntegrityError:
        #     for item in items:
        #         try:
        #             item.save()
        #         except IntegrityError:
        #             continue
        return super(ImportData, self).form_valid(form)


class ExternalImport(View):
    def get(self, request, *args, **kwargs):
        url = 'https://jsonplaceholder.typicode.com/users'
        json = requests.get(url, verify=False)
        # data = json.loads(json)
        print(json)
