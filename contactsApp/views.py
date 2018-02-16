from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from .models import Contact
from .forms import ContactForm, SearchForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import requests


class Contacts(ListView):
    model = Contact
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
        context['page_title'] = 'Contacts list'
        url = 'http://breffi.ru/ru/about'
        r = requests.get(url, verify=False)
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


class ContactDelete(DeleteView):
    model = Contact
    template_name = 'contact_delete.html'
    success_url = reverse_lazy('contacts_list')
