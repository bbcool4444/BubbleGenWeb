# Generated by Django 4.1.3 on 2022-11-10 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0004_delete_car"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="level",
            unique_together={("number", "game")},
        ),
    ]