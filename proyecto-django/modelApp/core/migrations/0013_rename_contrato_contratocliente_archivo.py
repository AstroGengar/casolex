# Generated by Django 3.2.3 on 2021-06-20 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_contratocliente'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contratocliente',
            old_name='Contrato',
            new_name='archivo',
        ),
    ]
