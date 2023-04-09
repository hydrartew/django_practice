from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Brends, Reviews, Sizes, Sneakers, SneakersPhotos, Specifications


@admin.register(Brends)
class BrendsAdmin(admin.ModelAdmin):
    '''Бренды'''
    list_display = ('name', 'id')
    

class ReviewInline(admin.StackedInline):
    '''Отзывы в админке фильма'''
    model = Reviews
    extra = 1  # кол-во доп. (пустых) полей
    readonly_fields = ('name', 'email', 'parent')


class SneakersPhotosInline(admin.TabularInline):
    '''Фотографии в админке Кроссовок'''
    model = SneakersPhotos
    extra = 0
    readonly_fields = ('get_image', )
    
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="160" height="200"')

    get_image.short_description = "Изображение"
    
    

@admin.register(Sneakers)
class SneakersAdmin(admin.ModelAdmin):
    '''Кроссовки'''
    list_display = ('title', 'price', 'brends', 'url', 'get_image', 'draft')
    readonly_fields = ('get_image', )
    list_filter = ['brends']
    search_fields = ('title', 'brends__name')
    inlines = [SneakersPhotosInline, ReviewInline]
    save_on_top = True  # отображение кнопок сохранений сверху
    save_as = True  # возможность "Сохранить как новый объект"
    list_editable = ('draft', )
    
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="160" height="200"')

    get_image.short_description = "Изображение"
    

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    '''Отзывы к кроссовкам'''
    list_display = ("name", "email", "parent", "sneaker", "id")
    readonly_fields = ("name", "email")
    list_filter = ['sneaker']
    
    
@admin.register(Sizes)
class SizesAdmin(admin.ModelAdmin):
    '''Размеры'''
    list_display = ['name']
    ordering = ['name']
     

@admin.register(SneakersPhotos)
class SneakersPhotosAdmin(admin.ModelAdmin):
    '''Фотографии кроссовок'''
    list_display = ('sneaker', 'title', 'get_image')
    readonly_fields = ('get_image', )
    search_fields = ('sneaker', 'title__name')
    
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" height="100"')

    get_image.short_description = "Изображение"
    
   
@admin.register(Specifications)
class SpecificationsAdmin(admin.ModelAdmin):
    '''Характеристики модели'''
    list_display = ('name', 'gender_male', 'gender_female', 'color', 'country', 'composition')
      

admin.site.site_header = 'Админка'
admin.site.site_title = 'Админка'
admin.site.index_title = 'Админка сайта'