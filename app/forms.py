from django import forms

from .models import Item, F_Item, Reservation

class ItemForm(forms.ModelForm):
    """
    モデルフォーム構成クラス
    ・公式 モデルからフォームを作成する
    https://docs.djangoproject.com/ja/2.1/topics/forms/modelforms/
    """
    field_order=["F_name","I_name","vegetable","quontity","deadline","memo"]
    class Meta:
        model = Item
        fields = '__all__'

class F_ItemForm(forms.ModelForm):
    """
    モデルフォーム構成クラス
    ・公式 モデルからフォームを作成する
    https://docs.djangoproject.com/ja/2.1/topics/forms/modelforms/
    """
    field_order=["photo","vegetable","title","unit_amount","quontity","deadline","price","tags","memo"]
    class Meta:
        model = F_Item
        fields = ["photo","vegetable","title","unit_amount","quontity","deadline","price","tags","memo"]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': "form-control",
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': "form-control-file",
            }),
        }


class BookForm(forms.ModelForm):

    field_order=["quontity","memo",]
    class Meta:
        model = Reservation
        fields = ["quontity","memo",]

        # 以下のフィールド以外が入力フォームに表示される
        # AutoField
        # auto_now=True
        # auto_now_add=Ture
        # editable=False
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
