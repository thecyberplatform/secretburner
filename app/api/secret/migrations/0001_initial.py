# Generated by Django 5.1.1 on 2024-09-11 22:51

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Secret',
            fields=[
                ('secret_id', models.TextField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('secret_text', models.TextField(null=True)),
                ('expiry_seconds', models.IntegerField(default=3600)),
                ('burn_at', models.BigIntegerField(db_index=True)),
                ('passphrase_hash', models.TextField(null=True)),
                ('public_key', models.TextField(null=True)),
                ('request_id', models.TextField(db_index=True, null=True)),
                ('fulfilment_id', models.TextField(db_index=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('verify_id', models.TextField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('burn_at', models.BigIntegerField(db_index=True)),
                ('code', models.TextField(db_index=True, max_length=20)),
                ('verified_token', models.TextField(db_index=True, null=True)),
                ('sender_email_hash', models.TextField()),
                ('recipient_email_hash', models.TextField()),
            ],
        ),
    ]
