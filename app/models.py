import datetime

from django.db import models

from users.models import User

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Tags(models.Model):
    """
    # 商品につける訳あり理由 blankとnullはデフォルトfalseです
    """

    # 名前
    name = models.CharField(
        max_length=15,
    )

    # 説明（任意）
    description = models.TextField(
        blank=True,
        null=True,
    )

    def get_tag_name(self):
        return self.name


    def __str__(self):
        """
        # リストボックスや管理画面での表示
        """
        return self.name



    class Meta:
        """
        # 管理画面でのタイトル表示
        """
        verbose_name = '訳あり理由'
        verbose_name_plural = '訳あり理由'


class Vegetable(models.Model):
    """
    # システムで取り扱う野菜リスト
    # 野菜の旬の時期とかをもたせておいて自動で「旬」ていう訳あり理由が付くようにできればいいのに（野望）

    """

    # 名前
    name = models.CharField(
        max_length=10,
    )

    # 説明
    description = models.TextField(
        blank=True,
        null=True,
    )

    def __str__(self):
        """
        # リストボックスや管理画面での表示
        """
        return self.name

    class Meta:
        """
        # 管理画面でのタイトル表示
        """
        verbose_name = '取り扱い野菜'
        verbose_name_plural = '取り扱い野菜'


class Item(models.Model):
    """
    データ定義クラス
      各フィールドを定義する
    参考：
    ・公式 モデルフィールドリファレンス
    https://docs.djangoproject.com/ja/2.1/ref/models/fields/
    """
    # 施設名
    F_name = models.CharField(
        verbose_name='施設名',
        max_length=20,
        blank=True,
        null=True,
    )

    # 入力者氏名
    I_name = models.ForeignKey(
        User,
        verbose_name='入力者氏名',
        max_length=20,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    # サンプル項目2 メモ
    memo = models.TextField(
        verbose_name='備考',
        blank=True,
        null=True,
    )

    # サンプル項目3 整数
    quontity = models.IntegerField(
        verbose_name='何kgほしいか',
        blank=True,
        null=True,
    )

    # サンプル項目7 日付
    deadline = models.DateField(
        verbose_name='いつほしいか',
        blank=True,
        null=True,
    )

    # サンプル項目9 選択肢（固定）
    vege_choice = (
        (1, '人参'),
        (2, '大根'),
        (3, 'じゃがいも'),
        (4, 'キャベツ'),
        (5, 'ホウレンソウ'),
        (6, 'ピーマン'),
        (7, 'なんでもいい'),
    )

    vegetable = models.IntegerField(
        verbose_name='ほしい野菜',
        choices=vege_choice,
        blank=True,
        null=True,
    )
        # 作成者(ユーザー)
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='C_CreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 作成時間
    created_at = models.DateTimeField(
        verbose_name='作成時間',
        blank=True,
        null=True,
        editable=False,
    )

    # 更新者(ユーザー)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='C_UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 更新時間
    updated_at = models.DateTimeField(
        verbose_name='更新時間',
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.sample_1

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = '需要'
        verbose_name_plural = '需要'


class F_Item(models.Model):
    """
    データ定義クラス
      各フィールドを定義する
    参考：
    ・公式 モデルフィールドリファレンス
    https://docs.djangoproject.com/ja/2.1/ref/models/fields/
    """

    # 出品者（農場名をリレーション先からもってこられるようにしたい）
    I_name = models.ForeignKey(
        User,
        verbose_name='出品者',
        max_length=20,
        blank=True,
        null=False,
        on_delete=models.PROTECT,
    #    editable=False,
        related_name='F_exhibitor'
    )

    # 商品名
    title = models.CharField(
        verbose_name='商品名',
        max_length=25,
        blank=True,
        null=True,
    )

    # 販売単位
    unit_amount = models.CharField(
        verbose_name='１セット内容量',
        max_length=10,
        blank=False,
        null=False,
    )

    #ランク
    RANK = (
        (1, 'Aランク（一般流通品)'), # 一般流通品
        (2, 'Bランク（販売用訳あり品）'), # ロス野菜良品
        (3, 'Cランク（販売不適可品）'), # ロス野菜
        (4, 'Dランク（可食品）') # 非食用品
    )

    rank = models.IntegerField(
        choices = RANK,
        verbose_name = 'ランク',

    )

    # 訳あり理由（野菜の状態）
    tags = models.ManyToManyField(
        Tags,
        verbose_name='訳あり理由',
        blank=True,
        null=True,
    )

    # 商品詳細（任意）
    memo = models.TextField(
        verbose_name='備考',
        blank=True,
        null=True,
    )

    # 出品セット数
    quontity = models.PositiveIntegerField(
        verbose_name='出品セット数',
        blank=False,
        null=False,
        validators=[MinValueValidator(1,"1セット以上の出品をしてください")],
    )

    quontity_left = models.PositiveIntegerField(
        verbose_name='在庫',
        blank=True,
        null=True,
    #    editable=False,
    )

    price = models.PositiveIntegerField(
        verbose_name='セット単価（￥）',
        blank=False,
        null=False,
        default=0,
        editable=True, # 実験用
    )

    # 購入期限
    deadline = models.DateField(
        verbose_name='購入期限',
        blank=True,
        null=True,
        default=datetime.datetime.now() + datetime.timedelta(weeks=1)
    )

    vegetable = models.ForeignKey(
        Vegetable,
        verbose_name='野菜の種類',
        blank=False,
        null=False,
        on_delete=models.PROTECT,
    )

    photo = models.ImageField(
        verbose_name='写真（任意）',
        upload_to='f_items/',
        default=None,
        blank=True,
        null=True,
    )

    # 以下、管理項目

    # 作成者(ユーザー)
    created_by = models.ForeignKey(
        User,
        verbose_name='出品者',
        blank=True,
        null=True,
        related_name='F_CreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 作成時間
    created_at = models.DateTimeField(
        verbose_name='出品時間',
        blank=True,
        null=True,
        editable=False,
    )

    # 更新者(ユーザー)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='F_UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 更新時間
    updated_at = models.DateTimeField(
        verbose_name='更新時間',
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.I_name.username

    def get_filename(self):
        return os.path.basename(self.photo.name)

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = '商品'
        verbose_name_plural = '商品'


class Reservation(models.Model):

    subscriber = models.ForeignKey(
        User,
        verbose_name='購入者',
        blank=True,
        null=False,
        related_name='Subscriber',
        on_delete=models.PROTECT,
        editable=False,
    )
    created_at = models.DateTimeField(
        verbose_name='作成時間',
        blank=True,
        null=False,
        editable=False,
    )
    target = models.ForeignKey(
        F_Item,
        verbose_name='商品アイテム',
        blank=True,
        null=False,
        related_name='F_Item',
        on_delete=models.PROTECT,
        editable=False,
        to_field='id',
    )
    total_price = models.PositiveIntegerField(
        verbose_name='合計金額',
        blank=True,
        null=False,
    )
    quontity = models.PositiveIntegerField(
        verbose_name='購入セット数',
        blank=False,
        null=False,
        validators=[MinValueValidator(1,"1セット以上の購入をしてください")]
    )
    memo = models.TextField(
        verbose_name='備考',
        blank=True,
        null=True,
    )

    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.subscriber.full_name

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = '予約'
        verbose_name_plural = '予約'
