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
    paginate_by = 100

class CustomerDetailView(generic.DetailView):
    model = Customer

# Order
class OrderListView(generic.ListView):
    model = Order
    paginate_by = 100

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

        # for each chunk, read
        for r in reader:
            # if new branch, create branch
            create_branch (r['Branch'])

            # if new customer, create customer else update details
            create_customer (r['Customer Name'], r['Age'], r['Contact #'], r['Email'], r['Address'])

            # Create order 
            create_order (r['Contact #'], r['Branch'], r['Order #'], r['Order Date'], r['Delivery Date'], r['Total Amount'], r['Advance'], r['Balance'])

        # END LOOP
    # END LOOP


def create_branch (str_branch_name):
    try:
        new_branch = Branch.objects.get(branch_name = str_branch_name)
    except Branch.DoesNotExist:
        new_branch = Branch(branch_name = str_branch_name)
        new_branch.save()

# Check if customer already exists. 
# If not, create one. Returns True if created, False if did not create
def create_customer (str_first_name, str_age,str_phone_no,str_email, str_address):

    try:
        int_phone_no = int(str_phone_no)
    except ValueError:
        return False 

    try:
        int_age = int(str_age)
    except ValueError:
        int_age = None 

    try:
        new_customer =  Customer.objects.get(phone_number=int_phone_no)
    except Customer.DoesNotExist:
        new_customer = Customer(
                                phone_number = int_phone_no,
                                first_name = str_first_name,
                                email = str_email,
                                address=str_address,
                                age = int_age
        )
        new_customer.save()

    return True


# Crate Order 
def create_order (str_contact_number, str_order_branch, str_order_number, str_order_date, str_delivery_date, str_payment_total, str_payment_advance, str_payment_balance):

    try:
        int_order_number = int(str_order_number)
        int_contact_number = int(str_contact_number)
    except ValueError as e:
        print ("error converting string inputs to integer. Assigning dummy value")
        return False            

    # Create order Instance
    try:
        new_order = Order.objects.get(order_number=int_order_number) # if found, update details
    except Order.DoesNotExist: # else create a new instance
        new_order = Order() 

    try:
        new_order.order_number = int(str_order_number)
    except ValueError as e:
        print ("error converting "+str_order_number+" to integer. Assigning dummy value")
        return False            
    
    try:
        new_order.payment_total = float(str_payment_total)
    except ValueError as e:
        new_order.payment_total = None

    try:
        new_order.payment_advance = float(str_payment_advance)
    except ValueError as e:
        new_order.payment_advance = None

    try:
        new_order.payment_balance = float(str_payment_balance)
    except ValueError as e:
        new_order.payment_balance = None

    try:
        new_order.order_date = datetime.strptime(str_order_date, '%Y-%m-%d')
    except Exception as e:
        print ("Error creating new order date")

    try: 
        new_order.delivery_date = datetime.strptime(str_delivery_date, '%Y-%m-%d')
    except Exception as e: 
        print ("Error creating order delivery date")

    try:
        new_order.customer = Customer.objects.get(phone_number=int_contact_number) # if found, update details
    except Customer.DoesNotExist:
        new_order.customer = None

    try:
        new_order.order_branch = Branch.objects.get(branch_name=str_order_branch) # if found, update details
    except Branch.DoesNotExist:
        new_order.order_branch = Branch()

    new_order.save()
    return True
