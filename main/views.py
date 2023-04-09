from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView
from django.views.generic.base import View

from .forms import ReviewForm
from .models import Brends, Sneakers


class BrendsPrice:
    '''Сортировка по брендам'''
    def get_brends(self):
        return Brends.objects.all()

    def get_prices(self):
        return Sneakers.objects.filter(draft=False).values('price')


class SneakersView(BrendsPrice, ListView):
    """Список кроссовок"""

    queryset = Sneakers.objects.filter(draft=False)
    template_name = "sneakers/sneakers.html"


class SneakerDetailView(BrendsPrice, DetailView):
    """Полное описание модели"""

    def get(self, request, slug):
        sneaker = Sneakers.objects.get(url=slug)
        return render(request, "sneakers/sneaker_detail.html", {"sneaker": sneaker})


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)  # данные запроса из forms.py: name, email, text
        sneaker = Sneakers.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):  # если есть ключ 'parent'
                form.parent_id = int(request.POST.get('parent'))  # достаем значение ключа
            form.sneaker = sneaker
            form.save()
        return redirect(sneaker.get_absolute_url())