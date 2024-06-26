# Generated by Django 5.0.3 on 2024-03-28 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("airport", "0003_alter_airplane_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="airplane",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="airplanetype",
            options={"ordering": ["name"], "verbose_name": "airplane-type"},
        ),
        migrations.AlterModelOptions(
            name="airport",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="city",
            options={"ordering": ["name"], "verbose_name_plural": "cities"},
        ),
        migrations.AlterModelOptions(
            name="country",
            options={"ordering": ["name"], "verbose_name_plural": "countries"},
        ),
        migrations.AlterModelOptions(
            name="crew",
            options={"ordering": ["first_name", "last_name"]},
        ),
        migrations.AlterModelOptions(
            name="flight",
            options={
                "default_related_name": "flights",
                "ordering": ["departure_time", "arrival_time"],
            },
        ),
        migrations.AlterModelOptions(
            name="order",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AlterModelOptions(
            name="route",
            options={"ordering": ["source", "destination"]},
        ),
        migrations.AlterModelOptions(
            name="ticket",
            options={"default_related_name": "tickets", "ordering": ["row", "seat"]},
        ),
        migrations.AlterUniqueTogether(
            name="route",
            unique_together={("source", "destination")},
        ),
    ]
