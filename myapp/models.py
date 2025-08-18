from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('Technical', 'Technical Issue'),
        ('Hardware', 'Hardware Problem'),
        ('Software', 'Software Problem'),
        ('Access', 'Access Request'),
        ('Training', 'IT training Request'),
        ('Other', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Solved', 'Solved'),
    ]

    ticket_number = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES, default='technical')
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    solution_text = models.TextField(null=True, blank=True)
    approx_solving_time = models.CharField(max_length=100, blank=True, null=True)
    solved_time = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ticket_number} - {self.title}"


class ITChecklist(models.Model):
    task = models.TextField(verbose_name="Checklist Item")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.task[:50]
