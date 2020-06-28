from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import static
from django.conf import settings

from .models import Item,F_Item,Reservation
from .views import TopView,SupplyList,ReservationList,ItemReservationList,FarmerReservationList,CustomerView,FarmerView,ItemCreateView, ItemDetailView, ItemBookView, ItemBookConfirmView, ItemBookCompleteView, ItemCreateView, ItemUpdateView, ItemDeleteView, ReservationDetailView, ReservationDeleteView,ItemBookFailedView, ReservationDeleteFailedView,RankView, ContactFromView, ContactReultView

# アプリケーションのルーティング設定

urlpatterns = [
    path('', TopView.as_view(), name='index'),
    path('c_index/', CustomerView.as_view(template_name='app/c_index.html'), name='c_index'),
    path('f_index/', FarmerView.as_view(template_name='app/f_index.html'), name='f_index'),
    path('detail/<int:pk>/', ItemDetailView.as_view(template_name='app/f_item_detail.html'), name='detail'),
    path('detail/<int:pk>/book/', ItemBookView.as_view(template_name='app/f_item_book.html'), name='book'),
    path('detail/<int:pk>/book/confirm', ItemBookConfirmView.as_view(template_name='app/f_item_book_confirm.html'), name='book_confirm'),
    path('detail/<int:pk>/book/complete', ItemBookCompleteView.as_view(template_name='app/f_item_book_complete.html'), name='book_complete'),
    path('detail/<int:pk>/book/failed', ItemBookFailedView.as_view(template_name='app/f_item_book_failed.html'), name='book_failed'),
    path('ItemReservationList/<int:pk>/',ItemReservationList.as_view(template_name='app/item_reservation_list.html'),name = 'item_reservation_list'),
    path('FarmerReservationList/<int:pk>/',FarmerReservationList.as_view(template_name='app/farmer_reservation_list.html'),name = 'farmer_reservation_list'),
    path('create/', ItemCreateView.as_view(), name='create'),
    path('SupplyList/<int:pk>',SupplyList.as_view(template_name='app/supply_list.html'),name = 'supply_list'),
    path('ReservationList/<int:pk>/',ReservationList.as_view(template_name='app/reservation_list.html'),name = 'reservation_list'),
    path('reservation_detail/<int:pk>/', ReservationDetailView.as_view(template_name='app/reservation_detail.html'), name='reservation_detail'),
    path('reservation_delete/<int:pk>/', ReservationDeleteView.as_view(), name='reservation_cancel'),
    path('reservation_delete_failed/<int:pk>/', ReservationDeleteFailedView.as_view(template_name='app/reservation_delete_failed.html'), name='reservation_delete_failed'),
    path('f_create/', ItemCreateView.as_view(template_name='app/item_form.html'), name='F_create'),
    path('update/<int:pk>/', ItemUpdateView.as_view(template_name='app/item_form.html'), name='update'),
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='delete'),
    #    path('accounts/', include('django.contrib.auth.urls'),name='accounts'), #  追加
    #    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), # [追加]
    path('rank/',RankView.as_view(),name='rank'),
    path('contact/', ContactFromView.as_view(template_name='app/contact.html'), name='contact'),
    path('contact_result', ContactReultView.as_view(template_name='app/contact_results.html'), name='contact_result'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
