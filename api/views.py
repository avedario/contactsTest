from rest_framework import generics, mixins
from .serializers import ContactSerializer
from contactsApp.models import Contact


class APIContactsList(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class APIContactsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
