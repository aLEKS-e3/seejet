# Generated by Django 5.0.3 on 2024-03-30 06:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("airport", "0004_alter_airplane_options_alter_airplanetype_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="flight",
            options={"ordering": ["departure_time", "arrival_time"]},
        ),
        migrations.AlterModelOptions(
            name="ticket",
            options={"ordering": ["row", "seat"]},
        ),
        migrations.AlterUniqueTogether(
            name="route",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="ticket",
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name="flight",
            name="airplane",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="flights",
                to="airport.airplane",
            ),
        ),
        migrations.AlterField(
            model_name="flight",
            name="crew",
            field=models.ManyToManyField(related_name="flights", to="airport.crew"),
        ),
        migrations.AlterField(
            model_name="flight",
            name="route",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="flights",
                to="airport.route",
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="flight",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="airport.flight",
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="airport.order",
            ),
        ),
        migrations.AddConstraint(
            model_name="route",
            constraint=models.UniqueConstraint(
                fields=("source", "destination"), name="unique flight route"
            ),
        ),
        migrations.AddConstraint(
            model_name="ticket",
            constraint=models.UniqueConstraint(
                fields=("row", "seat", "flight"), name="unique flight ticket"
            ),
        ),
    ]
