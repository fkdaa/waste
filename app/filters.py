import django_filters
from django.db import models

from .models import Item
from .models import F_Item
from .models import Reservation



class OrderingFilter(django_filters.filters.OrderingFilter):
    """日本語対応"""
    descending_fmt = '%s （降順）'


class ItemFilterSet(django_filters.FilterSet):
    """
     django-filter 構成クラス
    https://django-filter.readthedocs.io/en/latest/ref/filterset.html
    """

    # 検索フォームの「並び順」の設定
    order_by = OrderingFilter(
        initial='作成時間',
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
        ),
        field_labels={
            'created_at': '作成時間',
            'updated_at': '更新時間',
        },
        label='並び順'
    )

    class Meta:
        model = F_Item
        # 一部フィールドを除きモデルクラスの定義を全て引用する
        exclude = ['created_at', 'updated_by', 'updated_at',"photo" ]
        # 文字列検索のデフォルトを部分一致に変更
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.TextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }

class ReservationFilterSet(django_filters.FilterSet):
    """
     django-filter 構成クラス
    https://django-filter.readthedocs.io/en/latest/ref/filterset.html
    """

    # 検索フォームの「並び順」の設定
    order_by = OrderingFilter(
        initial='購入日時',
        fields=(
            ('created_at', 'created_at'),
        ),
        field_labels={
            'created_at': '購入日時',
        },
        label='並び順'
    )

    class Meta:
        model = Reservation
        # 一部フィールドを除きモデルクラスの定義を全て引用する
        exclude = ['subscriber',]
        # 文字列検索のデフォルトを部分一致に変更
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.TextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }
