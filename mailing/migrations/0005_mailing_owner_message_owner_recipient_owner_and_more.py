# Generated by Django 5.1.2 on 2024-11-18 17:29

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0004_alter_mailing_options_alter_mailing_finish_send_at_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="mailing",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="mailing_owner",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец",
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="massages_owner",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец",
            ),
        ),
        migrations.AddField(
            model_name="recipient",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="recipients_owner",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец",
            ),
        ),
        migrations.AlterField(
            model_name="mailing",
            name="finish_send_at",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 11, 18, 20, 29, 37, 819459),
                verbose_name="Дата и время окончания отправки",
            ),
        ),
        migrations.AlterField(
            model_name="mailing",
            name="first_send_at",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 11, 18, 20, 29, 37, 819445),
                verbose_name="Дата и время первой отправки",
            ),
        ),
    ]
