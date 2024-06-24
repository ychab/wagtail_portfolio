# Generated by Django 5.0.6 on 2024-06-24 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_portfoliosettings_favicon_portfoliosettings_logo"),
    ]

    operations = [
        migrations.AddField(
            model_name="portfoliosettings",
            name="cookie_text",
            field=models.CharField(blank=True, default="", max_length=2048),
        ),
        migrations.AddField(
            model_name="portfoliosettings",
            name="cookie_title",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
    ]
