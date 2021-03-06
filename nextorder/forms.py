from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from .models import Customer, Product, Branch, Order, Document


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = '__all__'

