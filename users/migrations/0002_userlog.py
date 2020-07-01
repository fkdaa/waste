# Generated by Django 3.0.4 on 2020-07-01 02:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='タイムスタンプ')),
                ('label', models.CharField(blank=True, max_length=100, verbose_name='アクセス先')),
                ('purchase_time', models.DurationField(blank=True, editable=False, null=True, verbose_name='所要時間')),
                ('target', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
            },
        ),
    ]
