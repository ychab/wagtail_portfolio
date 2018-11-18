from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, RichTextFieldPanel, StreamFieldPanel,
)
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel

from portfolio.core.forms import ContactForm


class ServiceBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=128)
    text = blocks.TextBlock()
    icon = blocks.CharBlock(max_length=128)

    class Meta:
        template = 'home/blocks/service.html'
        icon = 'time'


class ProjectBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=128)
    subheading = blocks.CharBlock(
        max_length=128,
        required=False,
        help_text=_('Sous-titre dans la vue grille'),
    )
    intro = blocks.CharBlock(
        max_length=255,
        required=False,
        help_text=_('Sous-titre dans la vue modal (grand écran)'),
    )
    image = ImageChooserBlock()
    text = blocks.TextBlock(required=False)
    date = blocks.DateBlock(required=False)
    client = blocks.CharBlock(required=False)

    class Meta:
        template = 'home/blocks/project_grid.html'
        icon = 'date'


class TeamMemberBlock(blocks.StructBlock):
    name = blocks.CharBlock()
    job = blocks.CharBlock(required=False)
    photo = ImageChooserBlock()

    class Meta:
        template = 'home/blocks/team_member.html'
        icon = 'group'


class HomePage(Page):

    # Header
    header_lead = models.CharField(
        verbose_name=_('Slogan'),
        max_length=255,
        blank=True,
        default='',
    )
    header_heading = models.CharField(
        verbose_name=_('Titre'),
        max_length=128,
        default='',
    )
    header_slide = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Slide'),
        related_name='+',
    )

    # Service
    service_subheading = models.CharField(
        verbose_name=_('Sous-titre'),
        max_length=255,
        blank=True,
        default='',
    )
    services = StreamField(
        [('service', ServiceBlock())],
        null=True,
        blank=True,
    )

    # Project
    project_subheading = models.CharField(
        verbose_name=_('Sous-titre'),
        max_length=255,
        blank=True,
        default='',
    )
    projects = StreamField(
        [('project', ProjectBlock())],
        null=True,
        blank=True,
    )

    # About
    about_heading = models.CharField(
        verbose_name=_('Titre'),
        max_length=128,
        default='',
    )
    about_subheading = models.CharField(
        verbose_name=_('Sous-titre'),
        max_length=128,
        blank=True,
        default='',
    )
    about_text = RichTextField(blank=True)

    # Team
    team_heading = models.CharField(
        verbose_name=_('Titre'),
        max_length=128,
        default='',
    )
    team_subheading = models.CharField(
        verbose_name=_('Sous-titre'),
        max_length=128,
        blank=True,
        default='',
    )
    team_members = StreamField(
        [('member', TeamMemberBlock())],
        null=True,
        blank=True,
    )
    team_text = models.CharField(
        verbose_name=_('Texte'),
        max_length=512,
        blank=True,
        default='',
    )

    # Contact
    contact_subheading = models.CharField(
        verbose_name=_('Sous-titre'),
        max_length=128,
        blank=True,
        default='',
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('header_lead'),
                FieldPanel('header_heading'),
                ImageChooserPanel('header_slide'),
            ],
            heading=_('Entête'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('service_subheading'),
                StreamFieldPanel('services'),
            ],
            heading=_('Services'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('project_subheading'),
                StreamFieldPanel('projects'),
            ],
            heading=_('Projets'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('about_heading'),
                FieldPanel('about_subheading'),
                RichTextFieldPanel('about_text'),
            ],
            heading=_('À propos'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('team_heading'),
                FieldPanel('team_subheading'),
                FieldPanel('team_text'),
                StreamFieldPanel('team_members'),
            ],
            heading=_('Équipe'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('contact_subheading'),
            ],
            heading=_('Contact'),
        ),
    ]

    class Meta:
        db_table = 'portfolio_homepage'
        verbose_name = _("Page d'accueil")

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['contact_form'] = ContactForm()
        return context
