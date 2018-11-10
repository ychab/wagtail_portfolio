from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, RichTextFieldPanel,
)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet


class HomePage(Page):
    navbar_title = models.CharField(
        verbose_name=_('Navbar title'),
        max_length=255,
        blank=True,
        default='',
    )

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
        FieldPanel('navbar_title'),
        MultiFieldPanel(
            [
                FieldPanel('header_title'),
                FieldPanel('header_text'),
                ImageChooserPanel('header_image'),
            ],
            heading=_('Header'),
        ),
        InlinePanel('project_placements', label=_("Projects")),
        MultiFieldPanel(
            [
                FieldPanel('about_title'),
                RichTextFieldPanel('about_text'),
            ],
            heading=_('About'),
        ),
    ]


@register_snippet
class Project(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=255)
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

    def __str__(self):
        return self.title


class HomePageProjectPlacement(Orderable, models.Model):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='project_placements')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='+')

    panels = [
        SnippetChooserPanel('project'),
    ]

    def __str__(self):
        return self.page.title + " -> " + self.project.title

#
# class Projects(Page):
#     date = models.DateField("Post date", default=timezone.now)
#     body = RichTextField(blank=True)
#
#     content_panels = Page.content_panels + [
#         FieldPanel('date'),
#         FieldPanel('body', classname="full"),
#         InlinePanel('images', label=_('Images')),
#     ]
#
#     parent_page_types = ['timeline.Timeline']
#     subpage_types = []
#
#     class Meta:
#         db_table = 'privagal_gallery'
#         verbose_name = _("Gallery")
#
#     def delete(self, *args, **kwargs):
#         with transaction.atomic():
#             # We need to call model instance method BEFORE deleting the
#             # instance itself to delete image in cascade. This is worst for
#             # performance than using QuerySet manager but keep it stupid.
#             for image in self.images.all():
#                 image.delete()
#             super().delete(*args, **kwargs)
#
#     @property
#     def image_teaser(self):
#         return self.images.first()
#
#     @property
#     def teaser(self):
#         return loader.render_to_string(
#             'gallery/gallery_teaser.html',
#             {
#                 PAGE_TEMPLATE_VAR: self,
#             },
#         )
