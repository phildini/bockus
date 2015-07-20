from django.conf.urls import patterns, include, url

import readers.views

readerpatterns = patterns('',
    url(r'^$', readers.views.ReaderListView.as_view(), name='reader-list'),
    url(
        r'^(?P<pk>\d+)/$',
        readers.views.ReaderView.as_view(),
        name='reader-detail',
    ),
    url(
        r'^new$',
        readers.views.CreateReaderView.as_view(),
        name='reader-create',
    ),
    url(
        r'^edit/(?P<pk>\d+)/$',
        readers.views.EditReaderView.as_view(),
        name='reader-edit',
    ),
    url(
        r'^delete/(?P<pk>\d+)/$',
        readers.views.DeleteReaderView.as_view(),
        name='reader-delete',
    ),
)