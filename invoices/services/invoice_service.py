import uuid
from django.db import transaction
from invoices.models import Invoice, InvoiceItem


class InvoiceService:

    @staticmethod
    @transaction.atomic
    def generate_invoice_from_todos(user, todos):
        """
        Create invoice from list of todos
        """

        invoice = Invoice.objects.create(
            user=user,
            invoice_number=str(uuid.uuid4())[:8].upper(),
            status='generated',
            subtotal=0,
            total=0
        )

        total_amount = 0

        for todo in todos:
            item_price = InvoiceService.calculate_price(todo)

            item = InvoiceItem.objects.create(
                invoice=invoice,
                todo=todo,
                title=todo.title,
                description=todo.description,
                quantity=1,
                unit_price=item_price,
            )

            total_amount += item.total_price

        invoice.subtotal = total_amount
        invoice.total = total_amount
        invoice.save()

        return invoice
    
    @staticmethod
    def calculate_price(todo):
        """
        Example pricing logic
        """

        base_price = 100

        if todo.priority == 'high':
            return base_price * 2
        elif todo.priority == 'medium':
            return base_price * 1.5
        else:
            return base_price