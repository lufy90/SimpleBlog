# Generated by Django 5.2.4 on 2025-07-26 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("settings", "0005_sitesettings_enable_image_compression_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="powered_by_text",
            field=models.CharField(
                default="SimpleBlog", help_text="Text to show in footer", max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="powered_by_url",
            field=models.URLField(
                blank=True,
                default="https://github.com/lufy90/SimpleBlog",
                help_text="URL for the powered by link (optional)",
            ),
        ),
    ]
