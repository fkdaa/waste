from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, TemplateView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.template.loader import render_to_string

from .filters import ItemFilterSet
from .filters import ReservationFilterSet

from .forms import ItemForm
from .forms import F_ItemForm
from .forms import BookForm

from .models import Item
from .models import F_Item
from .models import Reservation
from .models import User

# 未ログインのユーザーにアクセスを許可する場合は、LoginRequiredMixinを継承から外してください。
#
# LoginRequiredMixin：未ログインのユーザーをログイン画面に誘導するMixin
# 参考：https://docs.djangoproject.com/ja/2.1/topics/auth/default/#the-loginrequired-mixin

class TopView(TemplateView):
    """
    購入が完了しました
    """
    template_name = "app/index.html"


class CustomerView(FilterView):
    """
    ビュー：一覧表示画面

    以下のパッケージを使用
    ・django-filter 一覧画面(ListView)に検索機能を追加
    https://django-filter.readthedocs.io/en/master/
    """
    model = F_Item

    # django-filter 設定
    filterset_class = ItemFilterSet
    # django-filter ver2.0対応 クエリ未設定時に全件表示する設定
    strict = False

    # 1ページの表示
    paginate_by = 10

    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """

        # 一覧画面内の遷移(GETクエリがある)ならクエリを出品・編集を確定する
        if request.GET:
            request.session['query'] = request.GET
        # 詳細画面・登録画面からの遷移(GETクエリはない)ならクエリを復元する
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)

    def get_queryset(self):
        """
        ソート順・デフォルトの絞り込みを指定
        """
        # デフォルトの並び順として、登録時間（降順）をセットする。
        return F_Item.objects.filter(deadline__gt=timezone.now(), quontity_left__gte=1).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'
        kwargs['user'] = self.request.user

        return super().get_context_data(object_list=object_list, **kwargs)


class FarmerView(LoginRequiredMixin, FilterView):
    """
    ビュー：一覧表示画面

    以下のパッケージを使用
    ・django-filter 一覧画面(ListView)に検索機能を追加
    https://django-filter.readthedocs.io/en/master/
    """
    model = F_Item

    # django-filter 設定
    filterset_class = ItemFilterSet
    # django-filter ver2.0対応 クエリ未設定時に全件表示する設定
    strict = False

    # 1ページの表示
    paginate_by = 10

    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """

        # 一覧画面内の遷移(GETクエリがある)ならクエリを出品・編集を確定する
        if request.GET:
            request.session['query'] = request.GET
        # 詳細画面・登録画面からの遷移(GETクエリはない)ならクエリを復元する
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)

    def get_queryset(self):
        """
        ソート順・デフォルトの絞り込みを指定
        """
        # デフォルトの並び順として、登録時間（降順）をセットする。
        return F_Item.objects.filter(deadline__gt=timezone.now(), quontity_left__gte=1).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'
        kwargs['user'] = self.request.user

        return super().get_context_data(object_list=object_list, **kwargs)


class ItemDetailView(DetailView):
    """
    ビュー：詳細画面
    """

    model = F_Item

    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        kwargs['user'] = self.request.user

        return super().get_context_data(**kwargs)


class ItemCreateView(LoginRequiredMixin, CreateView):
    """
    #ビュー：需要登録画面
    """
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        #登録処理
        """
        item = form.save(commit=False)
        item.created_by = self.request.user
        item.created_at = timezone.now()
        item.updated_by = self.request.user
        item.updated_at = timezone.now()
        item.save()

        return HttpResponseRedirect(self.success_url)


class ItemCreateView(LoginRequiredMixin, CreateView):
    """
    ビュー：商品登録画面
    """
    model = F_Item
    form_class = F_ItemForm

    def form_valid(self, form):
        """
        登録処理
        """
        item = form.save(commit=False)
        item.I_name = self.request.user
        item.quontity_left = item.quontity
        item.created_by = self.request.user
        item.created_at = timezone.now()
        item.updated_by = self.request.user
        item.updated_at = timezone.now()
        item.save()
        form.save_m2m()

        return HttpResponseRedirect(reverse_lazy('supply_list',args=(self.request.user.id,)))

    def get_initial(self):

        return {'price':0}


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    """
    ビュー：更新画面
    """
    model = F_Item
    form_class = F_ItemForm

    def form_valid(self, form):
        """
        更新処理
        """
        item = form.save(commit=False)
        item.quontity_left = item.quontity
        item.updated_by = self.request.user
        item.updated_at = timezone.now()
        item.save()
        form.save_m2m()

        return HttpResponseRedirect(reverse_lazy('supply_list',args=(self.request.user.id,)))


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    """
    ビュー：削除画面
    """
    model = F_Item

    def delete(self, request, *args, **kwargs):
        """
        削除処理
        """
        item = self.get_object()
        item.delete()

        return HttpResponseRedirect(reverse_lazy('supply_list',args=(self.request.user.id,)))


class ItemBookView(LoginRequiredMixin, FormView):
    """
    ビュー：購入画面
    """
    model = Reservation
    form_class = BookForm
    success_url = reverse_lazy('complete')

    def form_valid(self, form):

        if self.request.POST.get('next', '') == 'create':

            # 登録処理
            item = form.save(commit=False)
            item.target = F_Item.objects.get(pk=self.kwargs['pk'])
            #item.save()

            if item.target.quontity_left < item.quontity:
                return HttpResponseRedirect(reverse_lazy('book_failed',args=(self.kwargs['pk'],)))

            else:
                item.subscriber = self.request.user
                item.created_at = timezone.now()
                item.target.quontity_left = item.target.quontity_left - item.quontity
                item.total_price = item.target.price * item.quontity
                item.target.save()
                item.save()

                # メール送信
                from_email = 'vegebank14@gmail.com'#送信元
                subject_buy = "【VegiBank】購入内容のご確認（自動送信）" #購入に変えたほうがいいかも
                subject_sell= "【VegeBank】出品中の商品が購入されました（自動送信）"

                user_buy = self.request.user
                user_sell = item.target.I_name

                context_buy = {
                    #テンプレートに渡す項目
                    "user_name" : user_buy.username,
                    "item_name" : item.target.vegetable.name,
                    "vege_name" : item.target.title,
                    "item_unit" : item.target.unit_amount,
                    "item_quantity" : item.quontity,
                    "item_from" : user_sell.farm_name,
                    "item_fee" : item.total_price
                }
                context_sell = {
                    #テンプレートに渡す項目
                    "user_name" : user_sell.username,
                    "item_name" : item.target.vegetable.name,
                    "vege_name" : item.target.title,
                    "item_unit" : item.target.unit_amount,
                    "item_quantity" : item.quontity,
                    "item_to" : user_buy.username,
                    "item_fee" : item.total_price
                }

                message_buy = render_to_string('mail/toBuyer_buy.txt', context_buy)
                message_sell = render_to_string('mail/toSupplier_buy.txt', context_sell)

                user_buy.email_user(subject_buy, message_buy, from_email)
                user_sell.email_user(subject_sell, message_sell, from_email)

                return HttpResponseRedirect(reverse_lazy('book_complete',args=(self.request.user.id,)))

        else:
            return HttpResponseRedirect(reverse_lazy('detail',args=(self.request.user.id,)))

    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        context = super().get_context_data(**kwargs)
        context["f_item"] = F_Item.objects.get(pk=self.kwargs['pk'])
        context['user'] = self.request.user

        return context


class ItemBookConfirmView(LoginRequiredMixin, DetailView):
    """
    ボツ
    """
    def get_queryset(self):
        return Reservation.objects.filter(target_id=self.kwargs['pk'])


class ItemBookCompleteView(LoginRequiredMixin, CreateView):
    """
    購入が完了しました
    """
    form_class = BookForm
    template_name = "f_item_book_complete.html"

    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        kwargs['user'] = self.request.user

        return super().get_context_data(**kwargs)


class ItemBookFailedView(LoginRequiredMixin, CreateView):
    """
    購入に失敗しました
    """
    form_class = BookForm
    template_name = "f_item_book_failed.html"

    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        kwargs['pk'] = self.kwargs['pk']

        return super().get_context_data(**kwargs)



class ReservationDetailView(LoginRequiredMixin, DetailView):
    """
    ビュー：予約情報
    """

    model = Reservation

    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        reservation = Reservation.objects.get(pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context["f_item"] = F_Item.objects.get(pk=reservation.target_id)
        context['user'] = self.request.user

        return context


class SupplyList(LoginRequiredMixin, FilterView):
    model = F_Item

    # django-filter 設定
    filterset_class = ReservationFilterSet
    # django-filter ver2.0対応 クエリ未設定時に全件表示する設定
    strict = False

    # 1ページの表示
    paginate_by = 10

    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """

        # 一覧画面内の遷移(GETクエリがある)ならクエリを出品・編集を確定する
        if request.GET:
            request.session['query'] = request.GET
        # 詳細画面・登録画面からの遷移(GETクエリはない)ならクエリを復元する
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)

    def get_queryset(self):
        """
        ソート順・デフォルトの絞り込みを指定
        """
        # デフォルトの並び順として、登録時間（降順）をセットする。
        return F_Item.objects.filter(created_by=self.request.user, deadline__gt=timezone.now(),quontity_left__gte=1).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'
        return super().get_context_data(object_list=object_list, **kwargs)

class ItemReservationList(LoginRequiredMixin, FilterView):
    """
    ビュー：一覧表示画面

    以下のパッケージを使用
    ・django-filter 一覧画面(ListView)に検索機能を追加
    https://django-filter.readthedocs.io/en/master/
    """
    model = Reservation

    # django-filter 設定
    filterset_class = ReservationFilterSet
    # django-filter ver2.0対応 クエリ未設定時に全件表示する設定
    strict = False

    # 1ページの表示
    paginate_by = 10

    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """

        # 一覧画面内の遷移(GETクエリがある)ならクエリを出品・編集を確定する
        if request.GET:
            request.session['query'] = request.GET
        # 詳細画面・登録画面からの遷移(GETクエリはない)ならクエリを復元する
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)

    def get_queryset(self):
        """
        ソート順・デフォルトの絞り込みを指定
        """
        # デフォルトの並び順として、登録時間（降順）をセットする。

        return Reservation.objects.filter(target=F_Item.objects.get(pk=self.kwargs['pk'])).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'

        kwargs['pk'] = self.kwargs['pk']

        return super().get_context_data(object_list=object_list, **kwargs)

class ReservationList(LoginRequiredMixin, FilterView):
    """
    ビュー：一覧表示画面

    以下のパッケージを使用
    ・django-filter 一覧画面(ListView)に検索機能を追加
    https://django-filter.readthedocs.io/en/master/
    """
    model = Reservation

    # django-filter 設定
    filterset_class = ReservationFilterSet
    # django-filter ver2.0対応 クエリ未設定時に全件表示する設定
    strict = False

    # 1ページの表示
    paginate_by = 10

    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """

        # 一覧画面内の遷移(GETクエリがある)ならクエリを出品・編集を確定する
        if request.GET:
            request.session['query'] = request.GET
        # 詳細画面・登録画面からの遷移(GETクエリはない)ならクエリを復元する
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)

    def get_queryset(self):
        """
        ソート順・デフォルトの絞り込みを指定
        """
        # デフォルトの並び順として、登録時間（降順）をセットする。

        return Reservation.objects.filter(subscriber=self.request.user, target__deadline__gt=timezone.now()).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'

        return super().get_context_data(object_list=object_list, **kwargs)


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    """
    ビュー：削除画面
    """
    model = Reservation

    def delete(self, request, *args, **kwargs):
        """
        削除処理
        """
        item = self.get_object()
        item.delete()

        return HttpResponseRedirect(reverse_lazy('reservation_list',args=(self.request.user.id,)))

    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        reservation = Reservation.objects.get(pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context["f_item"] = F_Item.objects.get(pk=reservation.target_id)

        return context
