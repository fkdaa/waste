from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    カスタムユーザー データ定義クラス

    ユーザーの管理項目を増やしたい場合はここにフィールドを定義します。
    例：住所、電話番号など
    """

    # first_name、last_nameの代わりにfull_nameを用意する
    full_name = models.CharField(
        verbose_name='氏名',
        max_length=100,
        blank=True
    )

    # スタッフ権限のデフォルトをTrueに変更する
    # ※ 原則ログインして利用することを想定している。

    is_staff = models.BooleanField(
        _('staff status'),
        default=True,
    )

    farm_name = models.CharField(
        verbose_name='農場名',
        max_length=100,
        blank=True,
    )

    # get_full_name()の変更
    def get_full_name(self):
        if self.full_name:
            return self.full_name
        else:
            return self.username + '（氏名未登録）'

    # 選択リストでの表示
    def __str__(self):
        return self.get_full_name()

    def get_farm_name(self):
        if self.farm_name:
            return self.farm_name
        else:
            return self.username + '（農場名未登録）'

    # 選択リストでの表示

class UserLog(models.Model):

    # 作成者(ユーザー)
    target = models.ForeignKey(
        User,
        verbose_name='ユーザー',
        blank=True,
        null=True,
        related_name='user',
        on_delete=models.SET_NULL,
        #editable=False,
    )

    # 作成時間
    timestamp = models.DateTimeField(
        verbose_name='タイムスタンプ',
        blank=True,
        null=True,
        #editable=False,
    )

    label = models.CharField(
        verbose_name='アクセス先',
        max_length=100,
        blank=True,
    )

    purchase_time = models.DurationField(
        verbose_name='所要時間',
        blank=True,
        null=True,
        #editable=False,
    )




    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.label

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = 'ユーザーログ'
        verbose_name_plural = 'ユーザーログ'
