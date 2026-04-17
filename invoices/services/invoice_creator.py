from invoices.services.invoice_service import InvoiceService
from todos.models import Todo


def create_invoice_for_user(user):
    todos = Todo.objects.filter(user=user, status='completed')

    if not todos.exists():
        return None

    invoice = InvoiceService.generate_invoice_from_todos(
        user=user,
        todos=todos
    )

    return invoice