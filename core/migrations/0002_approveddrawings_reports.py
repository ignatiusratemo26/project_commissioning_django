# Generated by Django 5.1.4 on 2024-12-15 06:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ApprovedDrawings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "architectural",
                    models.FileField(upload_to="approved_drawings/architectural/"),
                ),
                (
                    "structural",
                    models.FileField(upload_to="approved_drawings/structural/"),
                ),
                (
                    "proposed_sewer",
                    models.FileField(upload_to="approved_drawings/sewer/"),
                ),
                (
                    "proposed_water",
                    models.FileField(upload_to="approved_drawings/water/"),
                ),
                (
                    "proposed_electricity",
                    models.FileField(upload_to="approved_drawings/electricity/"),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="approved_drawings",
                        to="core.project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Reports",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("eia", models.FileField(upload_to="reports/eia/")),
                ("nema", models.FileField(upload_to="reports/nema/")),
                ("nca", models.FileField(upload_to="reports/nca/")),
                ("fire", models.FileField(upload_to="reports/fire/")),
                ("water", models.FileField(upload_to="reports/water/")),
                ("electricity", models.FileField(upload_to="reports/electricity/")),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reports_files",
                        to="core.project",
                    ),
                ),
            ],
        ),
    ]
