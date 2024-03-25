# Generated by Django 5.0.3 on 2024-03-25 15:29

import airport.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("airport", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="city",
            options={"verbose_name_plural": "cities"},
        ),
        migrations.AlterModelOptions(
            name="country",
            options={"verbose_name_plural": "countries"},
        ),
        migrations.AddField(
            model_name="crew",
            name="portrait",
            field=models.ImageField(
                null=True, upload_to=airport.models.crew_image_path
            ),
        ),
        migrations.AlterField(
            model_name="airplane",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]