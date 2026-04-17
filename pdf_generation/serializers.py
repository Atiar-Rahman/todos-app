# pdf_generation/serializers.py

from rest_framework import serializers

class InvoiceItemSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    quantity = serializers.IntegerField(default=1)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

class InvoiceSerializer(serializers.Serializer):
    invoice_number = serializers.CharField(max_length=50)
    user = serializers.EmailField()  # Assuming user is provided via email
    status = serializers.ChoiceField(choices=[('draft', 'Draft'), ('generated', 'Generated'), ('paid', 'Paid'), ('cancelled', 'Cancelled')], default='draft')
    items = InvoiceItemSerializer(many=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)