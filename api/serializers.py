from rest_framework import serializers
from contactsApp.models import Contact


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ('name', 'company', 'email', 'phone', 'interest')
