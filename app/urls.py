from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import static
from django.conf import settings

from .models import Item,F_Item,Reservation
from .views import TopView,SupplyList,ReservationList,CustomerView,FarmerView,F_ItemCreateView, ItemDetailView, ItemBookView, ItemBookConfirmView, ItemBookCompleteView, ItemCreateView, F_ItemUpdateView, F_ItemDeleteView, ReservationDetailView, ReservationDeleteView

# アプリケーションのルーティング設定

urlpatterns = [
    path('', TopView.as_view(), name='index'),
    path('c_index/', CustomerView.as_view(template_name='app/c_index.html'), name='c_index'),
    path('f_index/', FarmerView.as_view(template_name='app/f_index.html'), name='f_index'),
    path('detail/<int:pk>/', ItemDetailView.as_view(template_name='app/f_item_detail.html'), name='detail'),
    path('detail/<int:pk>/book/', ItemBookView.as_view(template_name='app/f_item_book.html'), name='book'),
    path('detail/<int:pk>/book/confirm/', ItemBookConfirmView.as_view(template_name='app/f_item_book_confirm.html'), name='book_confirm'),
    path('detail/<int:pk>/book/complete/', ItemBookCompleteView.as_view(template_name='app/f_item_book_complete.html'), name='book_complete'),
    path('create/', ItemCreateView.as_view(), name='create'),
    path('SupplyList/<int:pk>',SupplyList.as_view(template_name='app/supply_list.html'),name = 'supply_list'),
    path('ReservationList/<int:pk>/',ReservationList.as_view(template_name='app/reservation_list.html'),name = 'reservation_list'),
    path('reservation_detail/<int:pk>/', ReservationDetailView.as_view(template_name='app/reservation_detail.html'), name='reservation_detail'),
    path('reservation_delete/<int:pk>/', ReservationDeleteView.as_view(), name='reservation_cancel'),
    path('f_create/', F_ItemCreateView.as_view(template_name='app/item_form.html'), name='F_create'),
    path('update/<int:pk>/', F_ItemUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', F_ItemDeleteView.as_view(), name='delete'),
    #    path('accounts/', include('django.contrib.auth.urls'),name='accounts'), #  追加
    #    path('admin/', admin.site.urls),
    #    path('accounts/', include('accounts.urls')), # [追加]
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)