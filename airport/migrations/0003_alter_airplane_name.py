# Generated by Django 5.0.3 on 2024-03-26 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("airport", "0002_alter_city_options_alter_country_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="airplane",
            name="name",
            field=models.CharField(max_length=255),
        ),
    ]