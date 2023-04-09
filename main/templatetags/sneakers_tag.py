from django import template
from main.models import Brends, Sneakers

register = template.Library()


@register.simple_tag()
def get_brends():
    """Вывод всех категорий"""
    return Brends.objects.all()


@register.inclusion_tag('sneakers/tags/last_sneaker.html')
def get_last_sneakers(count=5):
    sneakers = Sneakers.objects.order_by("id")[:count]
    return {"last_sneaker": sneakers}