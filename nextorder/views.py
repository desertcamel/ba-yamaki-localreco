from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required

from .models import Customer, Product, Branch, Order, Document
from django.urls import reverse_lazy

from .forms import DocumentForm
from . import client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import FileSystemStorage

import pandas as pd
import csv

# Create your views here.

def index(request):
    """
    View function for home page of site.
    """

    # Generate counts of some of the main objects
    num_branch=Branch.objects.all().count()
    num_customers=Customer.objects.all().count()
    num_products=Product.objects.all().count()
    num_orders=Order.objects.all().count()

    # SESSION TRACKER
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1


    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_branch':num_branch,'num_customers':num_customers,'num_products':num_products, 
        'num_orders':num_orders, 'num_visits':num_visits}, # num_visits appended
    )

# Branch
class BranchListView(generic.ListView):
    model = Branch
    paginate_by = 50

class BranchDetailView(generic.DetailView):
    model = Branch

# Customer
class CustomerListView(generic.ListView):
    model = Customer
    paginate_by = 50

class CustomerDetailView(generic.DetailView):
    model = Customer


# Order
class OrderListView(generic.ListView):
    model = Order
    paginate_by = 50

    def get_queryset(self):
        return Order.objects.all().order_by('-order_date')

class OrderDetailView(generic.DetailView):
    model = Order


# FORMS HANDLING
def data_upload(request):
 
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            handle_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('orders'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = DocumentForm()

    return render(request, 'nextorder/file_upload.html', {'form': form})



def handle_file(upfile):
    for chunk in upfile.chunks():
        decoded_file = chunk.decode('utf-8-sig').splitlines() 
        reader = csv.DictReader(decoded_file)

        for r in reader:
            # if new branch, create branch
            
            q = Branch.objects.filter(branch_name__iexact=r['Branch'])
            if q.count() == 0:
                new_branch = Branch(branch_name = r['Branch'])
                new_branch.save()
            
            # if new customer, create customer else update details
            q = Customer.objects.filter(phone_number__iexact=r['Contact #'])

            if q.count() == 0:
                new_customer = Customer(
                                        phone_number = r['Contact #'],
                                        first_name = r['Customer Name']
                )
                new_customer.save()

            # Create order 
            q = Order.objects.filter(order_number__iexact=r['Contact #'])

            if q.count() == 0:
                new_order = Order(order_number = r['Order #'],
                                  payment_total = r['Total Amount'],
                                  payment_advance = r['Advance'],
                                  payment_balance = r['Balance'],
                )

            new_order.customer = Customer.objects.get(phone_number=r['Contact #'])
            new_order.order_date = datetime.strptime(r['Order Date'], '%Y-%m-%d')
            new_order.delivery_date = datetime.strptime(r['Delivery Date'], '%Y-%m-%d')

            new_order.save()
            new_order.order_branch = Branch.objects.get(pk=1)
            new_order.save()

        # END LOOP
    # END LOOP

