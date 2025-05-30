# Generated by Django 5.1.1 on 2025-04-28 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('auteur', models.CharField(blank=True, max_length=255, null=True)),
                ('type_document', models.CharField(choices=[('livre', 'Livre imprimé'), ('periodique', 'Périodique'), ('cd', 'CD / Livre enregistré'), ('dvd', 'DVD / Blu-Ray')], max_length=20)),
                ('genre', models.CharField(blank=True, max_length=100, null=True)),
                ('disponible', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
