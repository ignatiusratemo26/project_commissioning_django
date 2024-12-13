from django.db import models
from django.contrib.auth.models import AbstractUser
from users.models import User



class Project(models.Model):
    name = models.CharField(max_length=255)
    location = models.JSONField()  # {'county': '...', 'constituency': '...', 'plot_number': '...'}
    scope = models.CharField(max_length=50, choices=[('Residential', 'Residential'), ('Commercial', 'Commercial'), ('Mixed-use', 'Mixed-use')])
    approved_docs = models.JSONField(default=dict)  # {'architectural': '', 'structural': '', ...}
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


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
