# Generated by Django 3.2.3 on 2021-06-21 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_rename_contrato_contratocliente_archivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contratocliente',
            name='presupuesto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presupuesto', to='core.presupuestocliente'),
        ),
    ]
