# Migration: suppression du modèle Garage (système compte/garage retiré)

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_add_garage'),
    ]

    operations = [
        migrations.DeleteModel(name='Garage'),
    ]
