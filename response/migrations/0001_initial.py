# Generated by Django 2.2.3 on 2019-07-19 10:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="CommsChannel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("channel_id", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="ExternalUser",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("app_id", models.CharField(max_length=50)),
                ("external_id", models.CharField(max_length=50)),
                ("display_name", models.CharField(max_length=50)),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"unique_together": {("owner", "app_id")}},
        ),
        migrations.CreateModel(
            name="Incident",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("report", models.CharField(max_length=200)),
                ("report_time", models.DateTimeField()),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField(blank=True, null=True)),
                (
                    "summary",
                    models.TextField(
                        blank=True,
                        help_text="What's the high level summary?",
                        null=True,
                    ),
                ),
                (
                    "impact",
                    models.TextField(
                        blank=True, help_text="What impact is this having?", null=True
                    ),
                ),
                (
                    "severity",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("1", "critical"),
                            ("2", "major"),
                            ("3", "minor"),
                            ("4", "trivial"),
                        ],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "lead",
                    models.ForeignKey(
                        blank=True,
                        help_text="Who is leading?",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="lead",
                        to="response.ExternalUser",
                    ),
                ),
                (
                    "reporter",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="reporter",
                        to="response.ExternalUser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PinnedMessage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message_ts", models.CharField(max_length=50)),
                ("text", models.TextField()),
                ("timestamp", models.DateTimeField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="response.ExternalUser",
                    ),
                ),
                (
                    "incident",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="response.Incident",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HeadlinePost",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message_ts", models.CharField(max_length=20, null=True)),
                (
                    "comms_channel",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="response.CommsChannel",
                    ),
                ),
                (
                    "incident",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="response.Incident",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="commschannel",
            name="incident",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="response.Incident"
            ),
        ),
        migrations.CreateModel(
            name="Action",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("details", models.TextField(blank=True, default="")),
                ("done", models.BooleanField(default=False)),
                (
                    "incident",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="response.Incident",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="response.ExternalUser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserStats",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("join_time", models.DateTimeField(null=True)),
                ("message_count", models.IntegerField(default=0)),
                (
                    "incident",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="response.Incident",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="response.ExternalUser",
                    ),
                ),
            ],
            options={"unique_together": {("incident", "user")}},
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("key", models.CharField(max_length=30)),
                ("time", models.DateTimeField()),
                ("repeat_count", models.IntegerField(default=0)),
                ("completed", models.BooleanField(default=False)),
                (
                    "incident",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="response.Incident",
                    ),
                ),
            ],
            options={"unique_together": {("incident", "key")}},
        ),
        migrations.CreateModel(
            name="IncidentExtension",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("key", models.CharField(max_length=50)),
                ("value", models.CharField(max_length=100)),
                (
                    "incident",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="response.Incident",
                    ),
                ),
            ],
            options={"unique_together": {("incident", "key")}},
        ),
    ]
