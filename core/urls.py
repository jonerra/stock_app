from django.conf.urls import patterns, include, url
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^user/', include('registration.backends.simple.urls')),
    url(r'^user/', include('django.contrib.auth.urls')),
    url(r'^stock/create/$', login_required(StockPost.as_view()), name='stock_create'),
    url(r'stock/$', login_required(StockList.as_view()), name='stock_list'),
    url(r'^stock/(?P<pk>\d+)/$', login_required(StockDetail.as_view()), name='stock_detail'),
    url(r'^stock/update/(?P<pk>\d+)/$', login_required(StockUpdate.as_view()), name='stock_update'),
    url(r'^stock/delete/(?P<pk>\d+)/$', login_required(StockDelete.as_view()), name='stock_delete'),
    url(r'^stock/(?P<pk>\d+)/review/create/$', login_required(CreateReview.as_view()), name='review_create'),
    url(r'^stock/(?P<stock_pk>\d+)/review/update/(?P<review_pk>\d+)/$', login_required(UpdateReview.as_view()), name='review_update'),
    url(r'^stock/(?P<stock_pk>\d+)/review/delete/(?P<review_pk>\d+)/$', login_required(DeleteReview.as_view()), name='review_delete'),
    url(r'^vote/$', login_required(VoteFormView.as_view()), name='vote'),
)