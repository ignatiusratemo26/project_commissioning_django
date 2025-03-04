# Generated by Django 5.1.4 on 2024-12-18 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_alter_project_approved_docs"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="eia_report",
            field=models.FileField(blank=True, null=True, upload_to="eia_reports/"),
        ),
        migrations.AddField(
            model_name="project",
            name="nca_cert",
            field=models.FileField(
                blank=True, null=True, upload_to="nca_certificates/"
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="nema_cert",
            field=models.FileField(
                blank=True, null=True, upload_to="nema_certificates/"
            ),
        ),
    ]
