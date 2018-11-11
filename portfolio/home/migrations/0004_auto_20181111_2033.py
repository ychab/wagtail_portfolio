# Generated by Django 2.1.3 on 2018-11-11 20:33

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0021_image_file_hash'),
        ('home', '0003_auto_20181111_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageProjectPlacement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
            ],
            options={
                'db_table': 'portfolio_homepage_project',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='titre')),
                ('teaser', models.CharField(max_length=255, verbose_name='Résumé')),
                ('date', models.DateField(blank=True, null=True)),
                ('text', models.TextField(blank=True)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'verbose_name': 'Projet',
                'db_table': 'portfolio_project',
            },
        ),
        migrations.AlterModelOptions(
            name='homepage',
            options={'verbose_name': "Page d'accueil"},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'Service'},
        ),
        migrations.AlterField(
            model_name='service',
            name='slug',
            field=models.SlugField(help_text='Nom unique de service', unique=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='title',
            field=models.CharField(max_length=255, verbose_name='titre'),
        ),
        migrations.AddField(
            model_name='homepageprojectplacement',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_placements', to='home.HomePage'),
        ),
        migrations.AddField(
            model_name='homepageprojectplacement',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='home.Project'),
        ),
    ]