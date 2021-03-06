from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator


class Contact(models.Model):
    phone_validator = RegexValidator('^\+?1?\d{9,15}$', "Некорректный телефонный номер")

    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    email = models.EmailField(
        max_length=100,
        unique=True
    )
    phone = models.CharField(
        max_length=20,
        validators=[phone_validator]
    )
    interest = models.CharField(max_length=255)
    externalID = models.IntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('contact_detail', kwargs={'pk': self.pk})
