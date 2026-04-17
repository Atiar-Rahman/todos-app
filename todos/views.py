from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from todos.models import Todo
from todos.serializers import TodosSerializer


class TodoViewSet(ModelViewSet):
    serializer_class = TodosSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        todo = serializer.save(user=self.request.user)

        #  invoice hook (future use)
        # generate_invoice(todo)