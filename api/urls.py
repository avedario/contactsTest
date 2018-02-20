from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import APIContactsList, APIContactsDetail

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/contacts/$', APIContactsList.as_view()),
    url(r'^api/contacts/(?P<pk>[0-9]+)/$', APIContactsDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
