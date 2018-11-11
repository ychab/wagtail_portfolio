from django.db import migrations

from .default_data import set_default_data


def load_default_data(apps, schema_editor):
    Site = apps.get_model('wagtailcore.Site')
    PortfolioSettings = apps.get_model('core.PortfolioSettings')
    HomePage = apps.get_model('home.HomePage')
    Service = apps.get_model('home.Service')

    set_default_data(HomePage, PortfolioSettings, Service, Site)


def reset_default_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_default_data, reset_default_data),
    ]
