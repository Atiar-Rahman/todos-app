from django.db import models
import uuid
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your models here.

class Todos(models.Model):
    # UUId primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    # Relation with user
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='todos')

    # core fields
    title = models.CharField(max_length=255)
    description = models.TextField()

    # Priority(optional but useful)
    PRIORITY_CHOICES = (
        ('low','Low'),
        ('medium','Medium'),
        ('high','High')
    )

    priority = models.CharField(max_length=20,choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField(blank=True, null=True)
    is_archived = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    # timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    # string representation
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'todos'
        managed = True
        verbose_name = 'todo'
        verbose_name_plural = 'todos'
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['user','is_completed','title'])
        ]




    

