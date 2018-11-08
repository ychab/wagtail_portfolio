from django.db import models, transaction
from django.template import loader
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, RichTextFieldPanel,
)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, PAGE_TEMPLATE_VAR, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet


class HomePage(Page):
    content_panels = Page.content_panels + [
        InlinePanel('project_placements', label="Projects"),
    ]


@register_snippet
class Project(models.Model):
    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        help_text=_("The page title as you'd like it to be seen by the public")
    )
    text = RichTextField(blank=True)
    # text = models.TextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        FieldPanel('title'),
        # FieldPanel('text'),
        RichTextFieldPanel('text'),
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
