# Generated by Django 5.1.4 on 2024-12-18 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_project_architectural_project_proposed_electricity_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="approved_docs",
            field=models.IntegerField(default=dict, editable=False),
        ),
    ]
