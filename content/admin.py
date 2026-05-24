from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.utils.html import format_html

from .models import Variable, Photo, Layout, Attraction, Card, Document, Article, Application


@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'is_active')
    list_display_links = ('title',)
    list_editable = ('is_active',)


@admin.register(Photo)
class PhotoAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('get_image', 'is_active', 'order')
    list_display_links = ('get_image',)
    list_editable = ('is_active', 'order')

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="100" width="100" style="object-fit: cover;">', obj.image.url)
        else:
            return "Картинка не загружена"

    get_image.short_description = 'Картинка'


@admin.register(Layout)
class LayoutAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('get_title', 'get_image', 'is_active', 'order')
    list_display_links = ('get_image',)
    list_editable = ('is_active', 'order')
    search_fields = ('title',)

    def get_title(self, obj):
        return obj.title if obj.title else f'Планировка #{obj.pk}'

    get_title.short_description = 'Заголовок'

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="100" width="100" style="object-fit: cover;">', obj.image.url)
        else:
            return "Планировка не загружена"

    get_image.short_description = 'Планировка'


@admin.register(Attraction)
class AttractionAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'get_image', 'is_active', 'order')
    list_display_links = ('title', 'get_image')
    list_editable = ('is_active', 'order')
    search_fields = ('title', 'text')

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="100" width="100" style="object-fit: cover;">', obj.image.url)
        else:
            return "Картинка не загружена"

    get_image.short_description = 'Картинка'


@admin.register(Card)
class CardAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'get_image', 'type', 'is_active', 'order')
    list_display_links = ('title', 'get_image')
    list_editable = ('is_active', 'order')
    list_filter = ('type',)
    search_fields = ('title', 'text')

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="100" width="100" style="object-fit: cover;">', obj.image.url)
        else:
            return "Картинка не загружена"

    get_image.short_description = 'Картинка'


@admin.register(Document)
class DocumentAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_display_links = ('title',)
    list_editable = ('is_active', 'order')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'title', 'date', 'is_active')
    list_display_links = ('title', 'get_image')
    list_editable = ('is_active',)
    ordering = ('-date',)
    search_fields = ('title',)
    prepopulated_fields = {"slug": ('title',)}

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="100" width="100" style="object-fit: cover;">', obj.image.url)
        else:
            return "Картинка не загружена"

    get_image.short_description = 'Картинка'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'sub', 'created_at', 'is_processed')
    list_display_links = ('name', 'phone')
    list_editable = ('is_processed',)
    ordering = ('-created_at',)
    search_fields = ('name', 'phone')
    list_filter = ('is_processed', 'sub', 'created_at')
