from django.db import models
from django.contrib.auth.models import AbstractUser
from users.models import User
from django.conf import settings

def get_approved_doc_path(instance, filename):
  # Use project ID and filename to construct a path within MEDIA_ROOT
  return f'approved_documents/{instance.id}/{filename}'

class Project(models.Model):
    name = models.CharField(max_length=255)
    location = models.JSONField()  # {'county': '...', 'constituency': '...', 'plot_number': '...'}
    scope = models.CharField(max_length=50, choices=[('Residential', 'Residential'), ('Commercial', 'Commercial'), ('Mixed-use', 'Mixed-use')])
    approved_docs = models.JSONField(default=dict)  # {'architectural': '', 'structural': '', ...}
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    ready_for_approval = models.BooleanField(default=False)
    approved_for_commissioning = models.BooleanField(default=False)
    approved_for_occupancy = models.BooleanField(default=False)

    def get_approved_doc_urls(self):
        urls = {}
        for key, value in self.approved_docs.items():
            if value:
                urls[key] = f'{settings.MEDIA_URL}{value}'
        return urls

    def __str__(self):
        return self.name
 

class ApprovedDrawings(models.Model):
    project = models.ForeignKey(Project, related_name='approved_drawings', on_delete=models.CASCADE)
    architectural = models.FileField(upload_to='approved_drawings/architectural/')
    structural = models.FileField(upload_to='approved_drawings/structural/', null=True, blank=True)
    proposed_sewer = models.FileField(upload_to='approved_drawings/sewer/', null=True, blank=True)
    proposed_water = models.FileField(upload_to='approved_drawings/water/', null=True, blank=True)
    proposed_electricity = models.FileField(upload_to='approved_drawings/electricity/', null=True, blank=True)

    def __str__(self):
        return f"Approved Drawings for {self.project.name}"


class Stakeholder(models.Model):
    ROLE_CHOICES = [
        ('Architect', 'Architect'),
        ('Engineer', 'Engineer'),
        ('Contractor', 'Contractor'),
    ]
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    practicing_number = models.CharField(max_length=255, unique=True)
    certificate = models.FileField(upload_to='certificates/')
    project = models.ForeignKey(Project, related_name='stakeholders', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.role}"


class CommissioningReport(models.Model):
    SYSTEM_CHOICES = [
        ('Overall System', 'Overall System'),
        ('Fire System', 'Fire System'),
        ('Electrical System', 'Electrical System'),
        ('Water Supply System', 'Water Supply System'),
        ('Drainage System', 'Drainage System'),
        ('Vertical Movement System', 'Vertical Movement System'),
        ('Ventilation System', 'Ventilation System'),
    ]
    project = models.ForeignKey(Project, related_name='reports', on_delete=models.CASCADE)
    system = models.CharField(max_length=100, choices=SYSTEM_CHOICES)
    rating = models.IntegerField()
    report_file = models.FileField(upload_to='reports/')

    def __str__(self):
        return f"{self.project.name} - {self.system}"


class OccupancyCertificate(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    certificate_file = models.FileField(upload_to='occupancy_certificates/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
