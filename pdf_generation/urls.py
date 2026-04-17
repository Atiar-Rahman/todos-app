# pdf_generation/urls.py

from django.urls import path
from .views import generate_invoice_pdf

urlpatterns = [
    path('generate-invoice/', generate_invoice_pdf, name='generate_invoice_pdf'),
]