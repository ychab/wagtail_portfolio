from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import (
    FieldPanel, TabbedInterface, ObjectList, RichTextFieldPanel,
)
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.fields import RichTextField


class ContactFormSubmission(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=128, blank=True, default='')
    message = models.TextField()

    datetime = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return '{} - {} - {}'.format(self.name, self.email, self.datetime)


@register_setting(icon='placeholder')
class PortfolioSettings(BaseSetting):
    navbar_title = models.CharField(
        verbose_name=_('Navbar title'),
        max_length=255,
        blank=True,
        default='',
    )

    seo_keywords = models.CharField(
        verbose_name=_('SEO keywords'),
        max_length=256,
        blank=True,
        default='',
    )
    seo_description = models.CharField(
        verbose_name=_('SEO description'),
        max_length=512,
        blank=True,
        default='',
    )

    facebook_url = models.URLField(blank=True, default='')
    twitter_url = models.URLField(blank=True, default='')
    google_plus_url = models.URLField(blank=True, default='')
    instagram_url = models.URLField(blank=True, default='')

    address = models.CharField(max_length=255, blank=True, default='')
    email = models.EmailField(
        help_text=_('The contact email to display in footer.'),
        blank=True,
        default='',
    )
    phone = models.CharField(max_length=128, blank=True, default='')
    email_form = models.EmailField(
        help_text=_('The email to send form submission.'),
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
        ObjectList(global_panels, heading=_('Global')),
        ObjectList(seo_panels, heading=_('SEO')),
        ObjectList(social_panels, heading=_('Social network')),
        ObjectList(contact_panels, heading=_('Contact')),
        ObjectList(timetable_panels, heading=_('Timetable')),
    ])

    class Meta:
        db_table = 'portfolio_settings'
        verbose_name = 'Portfolio'
