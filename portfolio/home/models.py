from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, RichTextFieldPanel,
    StreamFieldPanel)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from modelcluster.fields import ParentalKey

from portfolio.core.forms import ContactForm


class ServiceBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=128)
    description = blocks.TextBlock(required=False)
    icon = blocks.CharBlock(max_length=128)

    class Meta:
        template = 'home/blocks/service.html'


class ProjectBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=128)
    heading = blocks.CharBlock(max_length=255)
    date = blocks.DateBlock(required=False)
    text = blocks.TextBlock(blank=True)
    image = ImageChooserBlock()

    class Meta:
        template = 'home/blocks/project.html'


class TeamMemberBlock(blocks.StructBlock):
    name = blocks.CharBlock()
    job = blocks.CharBlock(required=False)
    photo = ImageChooserBlock()

    class Meta:
        template = 'home/blocks/team_member.html'
        icon = 'user'


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

    # service_description = models.CharField(
    #     verbose_name=_('Description'),
    #     max_length=255,
    #     blank=True,
    #     default='',
    # )
    services = StreamField(
        [
            ('description', blocks.CharBlock(required=False, max_length=255))
            ('service', ServiceBlock())
        ],
        null=True,
        blank=True,
    )

    # project_description = models.CharField(
    #     verbose_name=_('Description'),
    #     max_length=255,
    #     blank=True,
    #     default='',
    # )
    projects = StreamField(
        [
            ('description', blocks.CharBlock(required=False, max_length=255))
            ('project', ProjectBlock())
        ],
        null=True,
        blank=True,
    )

    about_title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        blank=True,
        default='',
    )
    about_text = RichTextField(blank=True)

    contact_description = models.CharField(
        verbose_name=_('Description'),
        max_length=255,
        blank=True,
        default='',
    )

    team_members = StreamField(
        [
            ('title', blocks.CharBlock(max_length=128))
            ('description', blocks.CharBlock(required=False, max_length=255))
            ('member', TeamMemberBlock())
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('header_title'),
                FieldPanel('header_text'),
                ImageChooserPanel('header_image'),
            ],
            heading=_('Entête'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('service_description'),
                InlinePanel('service_placements', label=_("Services")),
            ],
            heading=_('Service'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('project_description'),
                InlinePanel('project_placements', label=_("Projets")),
            ],
            heading=_('Projet'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('about_title'),
                RichTextFieldPanel('about_text'),
            ],
            heading=_('À propos'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('contact_description'),
            ],
            heading=_('Contact'),
        ),
        StreamFieldPanel('team_members'),
    ]

    class Meta:
        db_table = 'portfolio_homepage'
        verbose_name = _('Page d\'accueil')

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['contact_form'] = ContactForm()
        # Fix django meta model ordering bug??
        context['services'] = [p.service for p in self.service_placements.all().order_by('sort_order')]
        return context
