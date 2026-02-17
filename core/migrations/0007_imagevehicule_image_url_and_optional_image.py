# Migration: ImageVehicule peut avoir un fichier OU une URL

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_garage'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagevehicule',
            name='image_url',
            field=models.URLField(blank=True, help_text='Lien vers une image si pas de fichier uploadé.', max_length=500, verbose_name='URL image (externe)'),
        ),
        migrations.AlterField(
            model_name='imagevehicule',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='vehicules/galerie/'),
        ),
    ]
