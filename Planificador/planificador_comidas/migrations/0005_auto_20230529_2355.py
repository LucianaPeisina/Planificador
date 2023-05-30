# Generated by Django 3.2.14 on 2023-05-30 02:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planificador_comidas', '0004_remove_miembro_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='comida',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='planificador_comidas.comida'),
        ),
        migrations.AlterField(
            model_name='elementocompra',
            name='compra',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='planificador_comidas.compra'),
        ),
        migrations.AlterField(
            model_name='miembro',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
