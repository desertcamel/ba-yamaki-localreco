from django.contrib import admin

# Register your models here.
from .models import Customer, Product, Branch, Order

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Branch)
admin.site.register(Order)