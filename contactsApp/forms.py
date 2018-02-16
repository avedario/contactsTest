from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    name = forms.CharField(
        required=True,
    )
    company = forms.CharField(
        required=True,
    )
    email = forms.EmailField(required=True)
    phone = forms.RegexField(
        '^\+?1?\d{11,15}$',
    )
    interest = forms.CharField(
        required=True,
    )

    class Meta:
        model = Contact
        fields = ('name', 'company', 'email', 'phone', 'interest')


class SearchForm(forms.Form):

    query = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Search by name or company'})
    )

    class Meta:
        fields = ('query',)
