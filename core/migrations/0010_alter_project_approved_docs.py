# Generated by Django 5.1.4 on 2024-12-18 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_project_eia_report_project_nca_cert_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="approved_docs",
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
