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


class TeamMemberBlock(blocks.StructBlock):
    name = blocks.CharBlock()
    job = blocks.CharBlock(required=False)
    photo = ImageChooserBlock()

    class Meta:
        template = 'home/blocks/team_member.html'
        icon='user'


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

    service_description = models.CharField(
        verbose_name=_('Description'),
        max_length=255,
        blank=True,
        default='',
    )

    project_description = models.CharField(
        verbose_name=_('Description'),
        max_length=255,
        blank=True,
        default='',
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


@register_snippet
class Service(models.Model):
    title = models.CharField(verbose_name=_('titre'), max_length=255)
    slug = models.SlugField(unique=True, help_text=_('Nom unique de service'))
    text = models.TextField(blank=True)
    icon = models.CharField(max_length=128)

    panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        FieldPanel('text'),
        FieldPanel('icon'),
    ]

    class Meta:
        db_table = 'portfolio_service'
        verbose_name = _('Service')

    def __str__(self):
        return self.title


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


@register_snippet
class Project(models.Model):
    title = models.CharField(verbose_name=_('titre'), max_length=255)
    teaser = models.CharField(verbose_name=_('Résumé'), max_length=255)
    date = models.DateField(null=True, blank=True)
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
        FieldPanel('teaser'),
        FieldPanel('date'),
        FieldPanel('text'),
        ImageChooserPanel('image'),
    ]

    class Meta:
        db_table = 'portfolio_project'
        verbose_name = _('Projet')

    def __str__(self):
        return self.title


class HomePageProjectPlacement(Orderable, models.Model):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='project_placements')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='+')

    panels = [
        SnippetChooserPanel('project'),
    ]

    class Meta:
        db_table = 'portfolio_homepage_project'

    def __str__(self):
        return self.page.title + " -> " + self.project.title

#
# @register_snippet
# class TeamMember(models.Model):
#     name = models.CharField(verbose_name=_('Nom'), max_length=255)
#     job = models.CharField(verbose_name=_('Fonction'), max_length=255)
#     photo = models.ForeignKey(
#         'wagtailimages.Image',
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='+',
#     )
#
#     panels = [
#         FieldPanel('name'),
#         FieldPanel('job'),
#         ImageChooserPanel('photo'),
#     ]
#
#     class Meta:
#         db_table = 'portfolio_team_member'
#         verbose_name = _('Équipier')
#
#     def __str__(self):
#         return self.name
#
#
# class HomePageTeamMemberPlacement(Orderable, models.Model):
#     page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='team_members_placements')
#     member = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='+')
#
#     panels = [
#         SnippetChooserPanel('member'),
#     ]
#
#     class Meta:
#         db_table = 'portfolio_homepage_team_member'
#
#     def __str__(self):
#         return self.page.title + " -> " + self.member.name
