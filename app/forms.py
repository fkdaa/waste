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
    field_order=["photo","vegetable","rank","unit_amount","quontity","deadline","price","tags","memo"]
    class Meta:
        model = F_Item
        fields = ["photo","vegetable","rank","unit_amount","quontity","deadline","price","tags","memo"]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': "form-control",
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': "form-control-file",
            }),
            'tags': forms.CheckboxSelectMultiple(),
        }


class BookForm(forms.ModelForm):

    field_order=["quontity",]
    class Meta:
        model = Reservation
        fields = ["quontity",]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quontity'].initial = 1
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ContactForm(forms.Form):
    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class' : 'form-control',
            'placeholder' : "お問い合わせ内容",
        }),
    )
