# Generated by Django 3.0.6 on 2020-06-22 06:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='subscriber',
            field=models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='Subscriber', to=settings.AUTH_USER_MODEL, verbose_name='購入者'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='target',
            field=models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='F_Item', to='app.F_Item', verbose_name='商品アイテム'),
        ),
        migrations.AddField(
            model_name='item',
            name='I_name',
            field=models.ForeignKey(blank=True, max_length=20, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='入力者氏名'),
        ),
        migrations.AddField(
            model_name='item',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='C_CreatedBy', to=settings.AUTH_USER_MODEL, verbose_name='作成者'),
        ),
        migrations.AddField(
            model_name='item',
            name='updated_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='C_UpdatedBy', to=settings.AUTH_USER_MODEL, verbose_name='更新者'),
        ),
        migrations.AddField(
            model_name='f_item',
            name='I_name',
            field=models.ForeignKey(blank=True, max_length=20, on_delete=django.db.models.deletion.PROTECT, related_name='F_exhibitor', to=settings.AUTH_USER_MODEL, verbose_name='出品者'),
        ),
        migrations.AddField(
            model_name='f_item',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='F_CreatedBy', to=settings.AUTH_USER_MODEL, verbose_name='出品者'),
        ),
        migrations.AddField(
            model_name='f_item',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='app.Tags', verbose_name='タグ（PCではCtrlキーを押しながら複数選択可）'),
        ),
        migrations.AddField(
            model_name='f_item',
            name='updated_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='F_UpdatedBy', to=settings.AUTH_USER_MODEL, verbose_name='更新者'),
        ),
        migrations.AddField(
            model_name='f_item',
            name='vegetable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.Vegetable', verbose_name='野菜の種類'),
        ),
    ]
