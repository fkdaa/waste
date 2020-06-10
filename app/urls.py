from django.contrib import admin
from django.urls import include, path

from .models import Item,F_Item,Reservation
from .views import C_View,F_View,R_View,ItemFilterView,F_ItemCreateView, ItemDetailView, ItemBookView, ItemBookConfirmView, ItemBookCompleteView, ItemCreateView, ItemUpdateView, ItemDeleteView

# アプリケーションのルーティング設定

urlpatterns = [
    path('detail/<int:pk>/', ItemDetailView.as_view(template_name='app/f_item_detail.html'), name='detail'),
    path('detail/<int:pk>/book/', ItemBookView.as_view(template_name='app/f_item_book.html'), name='book'),
    path('detail/<int:pk>/book/confirm', ItemBookConfirmView.as_view(template_name='app/f_item_book_confirm.html'), name='book_confirm'),
    path('detail/<int:pk>/book/complete', ItemBookCompleteView.as_view(template_name='app/f_item_book_complete.html'), name='book_complete'),
    path('create/', ItemCreateView.as_view(), name='create'),
    path('C_View/',C_View,name = 'C_View'),
    path('F_View/',F_View,name = 'F_View'),
    path('R_View/',R_View,name = 'R_View'),
    path('f_create/', F_ItemCreateView.as_view(template_name='app/item_form.html'), name='F_create'),
    path('update/<int:pk>/', ItemUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='delete'),
    path('', ItemFilterView.as_view(), name='index'),
    #    path('accounts/', include('django.contrib.auth.urls'),name='accounts'), #  追加
    #    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), # [追加]
]
