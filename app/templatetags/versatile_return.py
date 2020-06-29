from urllib import parse
from django import template
from django.shortcuts import resolve_url

register = template.Library()


@register.simple_tag
def get_return_link(request):
    top_page = resolve_url('index')  # 最新の日記一覧
    referer = request.environ.get('HTTP_REFERER')  # これが、前ページのURL

    # URL直接入力やお気に入りアクセスのときはリファラがないので、トップぺージに戻す
    if referer:
        return referer

    return top_page
