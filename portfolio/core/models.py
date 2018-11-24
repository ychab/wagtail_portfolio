from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, ObjectList, RichTextFieldPanel,
    TabbedInterface,
)
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel


@register_setting(icon='placeholder')
class PortfolioSettings(BaseSetting):
    navbar_title = models.CharField(
        verbose_name=_('Titre menu'),
        max_length=255,
        blank=True,
        default='',
    )

    seo_keywords = models.CharField(
        verbose_name=_('Mots clés SEO'),
        max_length=256,
        blank=True,
        default='',
    )
    seo_description = models.CharField(
        verbose_name=_('Description SEO'),
        max_length=512,
        blank=True,
        default='',
    )
    google_analytics_id = models.CharField(
        verbose_name=_('Google Analytics ID'),
        max_length=128,
        blank=True,
        default='',
    )

    lb_brand = models.CharField(
        verbose_name=_('Marque'),
        max_length=128,
        blank=True,
        default='',
    )
    lb_opening_hours = models.CharField(
        verbose_name=_('Horaires'),
        help_text=_('Exemple: Mo,Tu,We,Th,Fr,Sa 10:00-20:30'),
        max_length=128,
        blank=True,
        default='',
    )
    lb_polygon = models.CharField(
        verbose_name=_('Zone de couverture'),
        help_text=_('Au format polygone. Outil: https://www.doogal.co.uk/polylines.php. Exemple: -1.4585973651364839,47.24680912120602,0 -1.4531042010739839,47.24121534312366,0 -1.3267614276364839,47.83271445708654,0 -1.9969274432614839,47.86404914329155,0 -1.9831945331052339,47.29153808284894,0 -1.4585973651364839,47.24680912120602,0'),
        max_length=512,
        blank=True,
        default='',
    )
    lb_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Local Business Image'),
        related_name='+',
    )

    facebook_url = models.URLField(blank=True, default='')
    twitter_url = models.URLField(blank=True, default='')
    google_plus_url = models.URLField(blank=True, default='')
    instagram_url = models.URLField(blank=True, default='')

    address = models.CharField(max_length=255, blank=True, default='')
    email = models.EmailField(
        help_text=_('L\'adresse email affiché en pied de page.'),
        blank=True,
        default='',
    )
    phone = models.CharField(max_length=128, blank=True, default='')
    email_form = models.EmailField(
        help_text=_('L\'adresse email de contact du formulaire.'),
        blank=True,
        default='',
    )

    timetable = RichTextField(blank=True)

    global_panels = [
        FieldPanel('navbar_title'),
    ]
    seo_panels = [
        FieldPanel('seo_keywords'),
        FieldPanel('seo_description'),
        MultiFieldPanel(
            [
                FieldPanel('google_analytics_id'),
            ],
            heading=_('Google Analytics'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('lb_brand'),
                FieldPanel('lb_opening_hours'),
                FieldPanel('lb_polygon'),
                ImageChooserPanel('lb_image')
            ],
            heading=_('Local Business (Google)'),
        ),
    ]
    social_panels = [
        FieldPanel('facebook_url'),
        FieldPanel('twitter_url'),
        FieldPanel('google_plus_url'),
        FieldPanel('instagram_url'),
    ]
    contact_panels = [
        FieldPanel('address'),
        FieldPanel('email'),
        FieldPanel('phone'),
        FieldPanel('email_form'),
    ]
    timetable_panels = [
        RichTextFieldPanel('timetable'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(global_panels, heading=_('Générale')),
        ObjectList(seo_panels, heading=_('SEO')),
        ObjectList(social_panels, heading=_('Réseaux sociaux')),
        ObjectList(contact_panels, heading=_('Contact')),
        ObjectList(timetable_panels, heading=_('Horaires')),
    ])

    class Meta:
        db_table = 'portfolio_settings'
        verbose_name = 'Portfolio'


class ContactFormSubmission(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=128, blank=True, default='')
    message = models.TextField()

    datetime = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return '{} - {} - {}'.format(self.name, self.email, self.datetime)
