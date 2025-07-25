# Generated by Django 5.2.4 on 2025-07-26 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("settings", "0002_sitesettings_allow_anonymous_comments_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="show_attached_files_public",
            field=models.BooleanField(
                default=True,
                help_text="Show attached files section on public post detail pages",
            ),
        ),
    ]
