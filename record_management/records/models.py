from django.db import models
from django.contrib.auth.models import AbstractUser

class UserRecord(AbstractUser):
    ROLE_CHOICES = (
        ('administrative', 'Administrative'),
        ('division', 'Division'),
        ('service', 'Service'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Add related_name arguments to resolve clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_records',  # Change this to a unique related name
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_records',  # Change this to a unique related name
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username

class Document(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()  # Example of adding a description field
    pdf_file = models.FileField(upload_to='pdfs/')  # Example of adding a PDF file field


    def __str__(self):
        return self.title