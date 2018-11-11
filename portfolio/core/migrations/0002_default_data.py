from django.db import migrations


def load_default_data(apps, schema_editor):
    Site = apps.get_model('wagtailcore.Site')
    PortfolioSettings = apps.get_model('core.PortfolioSettings')
    HomePage = apps.get_model('home.HomePage')
    Service = apps.get_model('home.Service')

    # Set site
    site = Site.objects.first()
    site.site_name = 'Éducanine Nord Loire'
    site.save()

    # Set settings
    portfolio_settings, created = PortfolioSettings.objects.get_or_create(site=site)

    portfolio_settings.navbar_title = 'Éducanine Nord Loire'
    portfolio_settings.seo_keywords = 'Éducateur canin, Éducation canine, Dresseur de chien, Dressage chien, Loire-Atlantique, Nord-Loire, obéissance chien'
    portfolio_settings.seo_description = ''

    portfolio_settings.facebook_url = 'https://facebook.com'
    portfolio_settings.twitter_url = 'https://twitter.com'
    portfolio_settings.google_plus_url = 'https://googleplus.com'
    portfolio_settings.instagram_url = 'https://instagram.com'

    portfolio_settings.address = ''
    portfolio_settings.email = 'test@example.com'
    portfolio_settings.phone = '02 40 40 40 40'
    portfolio_settings.email_form = 'test@example.com'

    portfolio_settings.timetable = """
<p>Mes horaires d\'ouverture sont:
    <ul>
        <li>Du lundi au vendredi de 9h à 18h</li>
        <li>Le samedi matin de 9h à 12h</li>
    </ul>
</p>
"""

    portfolio_settings.save()

    # Homepage
    homepage = HomePage.objects.first()
    homepage.title = 'Page d\'accueil'

    homepage.header_title = 'Éducanine Nord Loire'
    homepage.header_text = 'Nelly Chabbert, éducateur canin du réseau Éducanine'

    homepage.about_title = 'À propos de nous'
    homepage.about_text = """
<p>
Avec mes chiens:
<ul>
    <li>Diablo</li>
    <li>Sparrow</li>
</ul>
nous formons une sacrée équipe pour vous accompagner dans l'éducation de votre chien.
</p>    
"""
    homepage.save()

    # Create services
    service1, created = Service.objects.get_or_create(slug='cours')
    service1.title = 'Cours d\'éducation canine'
    service1.text = 'Je vous propose des cours à domicile et en extérieur (parcs)'
    service1.save()

    service2, created = Service.objects.get_or_create(slug='evaluation')
    service2.title = 'Évaluation'
    service2.text = 'J\'effectue une évaluation de votre chien et vous propose des solutions'
    service2.save()

    service3, created = Service.objects.get_or_create(slug='ballade')
    service3.title = 'Ballade éducative'
    service3.text = 'Vous n\'arrivez plus à vous ballader avec votre chien ? Je peux vous aidder...'
    service3.save()

    service4, created = Service.objects.get_or_create(slug='vente')
    service4.title = 'Ventes de produits'
    service4.text = 'Alimentation, etc'
    service4.save()

    homepage.service_placements.set([
        service1,
        service2,
        service3,
        service4,
    ])


def reset_default_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_default_data, reset_default_data),
    ]
