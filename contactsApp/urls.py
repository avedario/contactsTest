from django.conf.urls import url
from .views import Contacts, ContactNew, ContactDetail, ContactEdit, ContactDelete,\
                   ExportData, ImportData, ExternalImport


urlpatterns = [
    url(r'^$', Contacts.as_view(), name='contacts_list'),
    url(r'^new$', ContactNew.as_view(), name='contact_new'),
    url(r'^detail/(?P<pk>\d+)$', ContactDetail.as_view(), name='contact_detail'),
    url(r'^edit/(?P<pk>\d+)$', ContactEdit.as_view(), name='contact_edit'),
    url(r'^delete/(?P<pk>\d+)$', ContactDelete.as_view(), name='contact_delete'),
    url(r'^export$', ExportData.as_view(), name='export_data'),
    url(r'^import$', ImportData.as_view(), name='import_data'),
    url(r'^external_import$', ExternalImport.as_view(), name='external_import'),
]
