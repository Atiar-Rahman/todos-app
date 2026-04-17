from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from todos.models import Todo
from todos.serializers import TodoSerializer
from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
class TodoViewSet(ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

   

    @action(detail=True, methods=['get','post'])
    def generate_invoice(self, request, pk=None):
        """
        Generate a PDF invoice for the given Todo item.
        """
        todo = self.get_object()

        # Convert the Todo instance to a dictionary
        todo_data = {
            'times':10,
            'title': todo.title,
            'description': todo.description,
            'priority': todo.priority,
            'due_date': todo.due_date,
            'status': todo.status,
        }

        # Render the HTML template to generate the content
        html_content = render_to_string('hello.html', todo_data)

        try:
            # Generate PDF using WeasyPrint
            pdf = HTML(string=html_content).write_pdf()

            # Return PDF as a response for download
            response = HttpResponse(pdf, content_type='application/pdf')

            # Set the Content-Disposition to 'attachment' to force the download
            response['Content-Disposition'] = f'attachment; filename="invoice_{todo.title}.pdf"'

            return response

        except Exception as e:
            # Log the error if something goes wrong
            print(f"Error generating PDF: {e}")
            return Response(
                {"error": "Failed to generate PDF"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )