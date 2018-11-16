# Generated by Django 2.1.3 on 2018-11-15 11:42

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0021_image_file_hash'),
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='homepage',
            options={'verbose_name': "Page d'accueil"},
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_heading',
            field=models.CharField(default='', max_length=128, verbose_name='Titre'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_subheading',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='Sous-titre'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='about_text',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='contact_subheading',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='Sous-titre'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='header_heading',
            field=models.CharField(default='', max_length=128, verbose_name='Titre'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='header_lead',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Slogan'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='header_slide',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Slide'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='project_subheading',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Sous-titre'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='projects',
            field=wagtail.core.fields.StreamField([('project', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(max_length=128)), ('subheading', wagtail.core.blocks.CharBlock(help_text='Sous-titre dans la vue grille', max_length=128, required=False)), ('intro', wagtail.core.blocks.CharBlock(help_text='Sous-titre dans la vue modal (grand écran)', max_length=255, required=False)), ('image', wagtail.images.blocks.ImageChooserBlock()), ('text', wagtail.core.blocks.TextBlock(required=False)), ('date', wagtail.core.blocks.DateBlock(required=False)), ('client', wagtail.core.blocks.CharBlock(required=False))]))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='service_subheading',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Sous-titre'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='services',
            field=wagtail.core.fields.StreamField([('service', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(max_length=128)), ('text', wagtail.core.blocks.TextBlock()), ('icon', wagtail.core.blocks.CharBlock(max_length=128))]))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='team_heading',
            field=models.CharField(default='', max_length=128, verbose_name='Titre'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='team_members',
            field=wagtail.core.fields.StreamField([('member', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock()), ('job', wagtail.core.blocks.CharBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock())]))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='team_subheading',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='Sous-titre'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='team_text',
            field=models.CharField(blank=True, default='', max_length=512, verbose_name='Texte'),
        ),
        migrations.AlterModelTable(
            name='homepage',
            table='portfolio_homepage',
        ),
    ]