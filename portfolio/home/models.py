from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, RichTextFieldPanel,
)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from modelcluster.fields import ParentalKey

from portfolio.core.forms import ContactForm


class HomePage(Page):
    header_title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        blank=True,
        default='',
    )
    header_text = models.TextField(verbose_name=_('Text'), blank=True)
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Image'),
        related_name='+',
    )

    about_title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        blank=True,
        default='',
    )
    about_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('header_title'),
                FieldPanel('header_text'),
                ImageChooserPanel('header_image'),
            ],
            heading=_('Header'),
        ),
        InlinePanel('service_placements', label=_("Services")),
        MultiFieldPanel(
            [
                FieldPanel('about_title'),
                RichTextFieldPanel('about_text'),
            ],
            heading=_('About'),
        ),
    ]

    class Meta:
        db_table = 'portfolio_homepage'

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['contact_form'] = ContactForm()
        return context


@register_snippet
class Service(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=255)
    slug = models.SlugField(unique=True, help_text=_('Unique name of the service'))
    text = models.TextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('text'),
        ImageChooserPanel('image'),
    ]

    class Meta:
        db_table = 'portfolio_service'

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            # We need to call model instance method BEFORE deleting the
            # instance itself to delete image in cascade.
            self.image.delete()
            super().delete(*args, **kwargs)


class HomePageServicePlacement(Orderable, models.Model):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='service_placements')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='+')

    panels = [
        SnippetChooserPanel('service'),
    ]

    class Meta:
        db_table = 'portfolio_homepage_service'

    def __str__(self):
        return self.page.title + " -> " + self.service.title
