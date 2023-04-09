from django.db import models
from django.urls import reverse


class Brends(models.Model):
    """Бренды"""

    name = models.CharField("Бренды", max_length=150)

    def __str__(self):
        return self.name

    class Meta:  # контейнер класса
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"


class Sizes(models.Model):
    """Таблица размеров"""

    name = models.CharField("Размер RU", max_length=100, unique=True)
    description = models.TextField("Описание", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"


class Specifications(models.Model):
    '''Характеристики модели'''
    name = models.CharField("Название модели", max_length=100)
    gender_male = models.BooleanField("Мужской", default=True)
    gender_female = models.BooleanField("Женский", default=False)
    color = models.CharField("Цвет", max_length=20)
    country = models.CharField("Страна", max_length=20)
    composition = models.CharField("Cостав", max_length=100, help_text="Пример: кожа, текстиль, резина...")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Характеристика | Шаблон"
        verbose_name_plural = "Характеристики | Шаблоны"


class Sneakers(models.Model):
    """Кроссовки"""

    draft = models.BooleanField("Черновик", default=False)
    title = models.CharField("Название", max_length=100)  # текстовое поле с ограничениями
    article_number = models.CharField("Артикул", max_length=10, help_text='макс. длина: 10 символов', unique=True)
    brief = models.CharField("Краткое описание", max_length=40, help_text='макс. длина: 40 символов')
    description = models.TextField("Описание")  # текстовое поле без ограничений
    specifications = models.ManyToManyField(Specifications, verbose_name="Характеристика", related_name="specification")
    brends = models.ForeignKey(Brends, verbose_name="Бренд", on_delete=models.SET_NULL, null=True)
    price = models.PositiveSmallIntegerField("Цена", default=0, help_text="указывать сумму в рублях")
    sizes = models.ManyToManyField(Sizes, verbose_name="Размеры", related_name="sizes")
    url = models.SlugField(max_length=130, unique=True)  # текстовое поле, сод. только буквы, цифры, дефисы и _ (url)
    image = models.ImageField("Картинка", upload_to="imgs/")

    def __str__(self):
        return self.title  # возвр. строковое представление нашей модели

    def get_absolute_url(self):
        return reverse("sneaker_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)  # список отзывов, прикреп. к модели с фильтрацией родителя

    class Meta:
        verbose_name = "Кроссовки"
        verbose_name_plural = "Кроссовки"


class SneakersPhotos(models.Model):
    """Фотографии кроссовок"""
    title = models.CharField("Заголовок", max_length=100)
    image = models.ImageField("Изображение", upload_to="sneaker_shots/")
    sneaker = models.ForeignKey(Sneakers, verbose_name="Кроссовки", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фото кроссовок"
        verbose_name_plural = "Фотографии кроссовок"
        

class Reviews(models.Model):
    """Отзывы"""
    
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    sneaker = models.ForeignKey(Sneakers, verbose_name="кроссовки", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.sneaker}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"