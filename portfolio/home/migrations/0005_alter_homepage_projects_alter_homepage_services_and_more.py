# Generated by Django 4.0.8 on 2022-12-15 20:33

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_homepage_project_heading'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='projects',
            field=wagtail.fields.StreamField([('project', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock(max_length=128)), ('subheading', wagtail.blocks.CharBlock(help_text='Sous-titre dans la vue grille', max_length=128, required=False)), ('intro', wagtail.blocks.CharBlock(help_text='Sous-titre dans la vue modal (grand écran)', max_length=255, required=False)), ('image', wagtail.images.blocks.ImageChooserBlock()), ('text', wagtail.blocks.TextBlock(required=False)), ('date', wagtail.blocks.DateBlock(required=False)), ('client', wagtail.blocks.CharBlock(required=False))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='services',
            field=wagtail.fields.StreamField([('service', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock(max_length=128)), ('text', wagtail.blocks.TextBlock()), ('icon', wagtail.blocks.CharBlock(max_length=128))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='team_members',
            field=wagtail.fields.StreamField([('member', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock()), ('job', wagtail.blocks.CharBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock())]))], blank=True, null=True),
        ),
    ]
