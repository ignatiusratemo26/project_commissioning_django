# Generated by Django 5.1.4 on 2024-12-18 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_alter_project_approved_docs"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="ready_for_commissioning",
            field=models.BooleanField(default=False),
        ),
    ]
