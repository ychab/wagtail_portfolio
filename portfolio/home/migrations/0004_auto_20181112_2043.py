# Generated by Django 2.1.3 on 2018-11-12 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20181111_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='project_intro',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Introduction'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='service_intro',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Introduction'),
        ),
    ]
