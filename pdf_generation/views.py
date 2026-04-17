from django.shortcuts import render

# Create your views here.
# pdf_generation/views.py

from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from weasyprint import HTML
from .serializers import InvoiceSerializer
from jinja2 import Template
from io import BytesIO

@api_view(['POST'])
def generate_invoice_pdf(request):
    """
    Generate a PDF for the invoice from the provided JSON data.
    """
    # Serialize and validate incoming data
    serializer = InvoiceSerializer(data=request.data)
    if serializer.is_valid():
        json_data = serializer.validated_data

        # Render HTML from JSON
        html_content = render_html_from_json(json_data)
        
        # Generate PDF from HTML
        pdf = generate_pdf_from_html(html_content)

        # Return PDF as HTTP response
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="invoice_{json_data["invoice_number"]}.pdf"'
        
        return response
    else:
        return JsonResponse(serializer.errors, status=400)


def render_html_from_json(json_data):
    """
    This function takes the JSON data and renders it using Jinja2 template.
    """
    # Path to your HTML template
    template_path = "pdf_generation/templates/invoice_template.html"

    # Read the HTML template
    with open(template_path, 'r') as file:
        template_content = file.read()

    # Use Jinja2 to render the HTML with JSON data
    template = Template(template_content)
    html_content = template.render(
        invoice_number=json_data["invoice_number"],
        user=json_data["user"],
        status=json_data["status"],
        items=json_data["items"],
        subtotal=json_data["subtotal"],
        total=json_data["total"]
    )

    return html_content


def generate_pdf_from_html(html_content):
    """
    This function takes the HTML content and generates a PDF using WeasyPrint.
    """
    pdf = HTML(string=html_content).write_pdf()
    return pdf

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import InvoiceSerializer

@api_view(['POST'])
def generate_invoice_pdf(request):
    try:
        # Deserialize data
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # Ensure the template exists
            html_content = render_to_string('invoice_template.html', data)

            # Generate PDF
            pdf = HTML(string=html_content).write_pdf()

            # Return PDF as a response
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="invoice_{data["invoice_number"]}.pdf"'
            return response
        else:
            return Response(serializer.errors, status=400)
    except FileNotFoundError as e:
        return HttpResponse(f"Error: Template file not found. Please ensure 'invoice_template.html' exists. Error: {str(e)}", status=500)
    except Exception as e:
        return HttpResponse(f"An unexpected error occurred: {str(e)}", status=500)
    


