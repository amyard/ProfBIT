# Generated by Django 2.2.2 on 2019-06-08 16:04

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20190608_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueueToDBModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('product_by_date', models.PositiveIntegerField(blank=True)),
                ('top_hundred', models.PositiveIntegerField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
