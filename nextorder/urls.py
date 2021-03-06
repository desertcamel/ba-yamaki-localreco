from django.conf.urls import include, url

from . import views


# Home Page
urlpatterns = [
    url(r'^$', views.index, name='index'),
]

# Branch Urls
urlpatterns += [
    # List
    url(r'^branches/$', views.BranchListView.as_view(), name='branches'),
    # Detail
    url(r'branch/(?P<pk>\d+)$', views.BranchDetailView.as_view(), name='branch-detail'),
]

# Customer Urls
urlpatterns += [
    # List
    url(r'^customers/$', views.CustomerListView.as_view(), name='customers'),
    # Detail
    url(r'customer/(?P<pk>\d+)$', views.CustomerDetailView.as_view(), name='customer-detail'),
]

# Order Urls
urlpatterns += [
    # List
    url(r'^orders/$', views.OrderListView.as_view(), name='orders'),
    # Detail
    url(r'order/(?P<pk>\d+)$', views.OrderDetailView.as_view(), name='order-detail'),
]


# Form Handling
urlpatterns += [   
    url(r'^data/$', views.data_upload, name='data-upload'),
]