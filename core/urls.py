from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^user/', include('registration.backends.simple.urls')),
    url(r'^user/', include('django.contrib.auth.urls')),
    url(r'^stock/create/$', StockPost.as_view(), name='stock_create'),
    url(r'stock/$', StockList.as_view(), name='stock_list'),
    url(r'^stock/(?P<pk>\d+)/$', StockDetail.as_view(), name='stock_detail'),
    url(r'^stock/update/(?P<pk>\d+)/$', StockUpdate.as_view(), name='stock_update'),
    url(r'^stock/delete/(?P<pk>\d+)/$', StockDelete.as_view(), name='stock_delete'),
    url(r'^stock/(?P<pk>\d+)/review/create/$', CreateReview.as_view(), name='review_create'),
)