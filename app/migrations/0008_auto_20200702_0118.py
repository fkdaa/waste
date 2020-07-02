# Generated by Django 3.0.6 on 2020-07-01 16:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20200702_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactlog',
            name='message',
            field=models.TextField(editable=False, verbose_name='お問い合わせ内容'),
        ),
        migrations.AlterField(
            model_name='f_item',
            name='deadline',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 7, 9, 1, 18, 41, 834549), null=True, verbose_name='購入期限'),
        ),
    ]
