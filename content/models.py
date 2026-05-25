import os
import re
from datetime import timezone

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from uuid import uuid4

from pathlib import Path
from django.utils.text import slugify


def path_to_variables_icons(instance, filename):
    ext = Path(filename).suffix
    filename = f"{uuid4()}{ext}"
    return os.path.join('variables', 'icons', filename)


def path_to_variables_images(instance, filename):
    filename = f"{uuid4()}.webp"
    return os.path.join('variables', 'images', filename)


def path_to_photos_images(instance, filename):
    filename = f"{uuid4()}.webp"
    return os.path.join('photos', filename)


def path_to_layouts_images(instance, filename):
    filename = f"{uuid4()}.webp"
    return os.path.join('layouts', filename)


def path_to_attraction_images(instance, filename):
    filename = f"{uuid4()}.webp"
    return os.path.join('attractions', filename)


def path_to_cards_images(instance, filename):
    filename = f"{uuid4()}.webp"
    return os.path.join('cards', filename)


def path_to_documents_files(instance, filename):
    ext = Path(filename).suffix
    filename = f"{uuid4()}.{ext}"
    return os.path.join('documents', filename)


def path_to_articles_images(instance, filename):
    filename = f"{uuid4()}.webp"
    return os.path.join('articles', filename)


class Variable(models.Model):
    class Meta:
        verbose_name = 'Переменная'
        verbose_name_plural = 'Переменные'
        ordering = ['order']

    title = models.CharField(max_length=255, blank=False, verbose_name='Имя переменной')
    text_1 = models.CharField(max_length=500, blank=True, verbose_name='Текст 1')
    text_2 = models.TextField(blank=True, verbose_name='Текст 2')
    text_3 = RichTextUploadingField(blank=True, verbose_name='Текст 3')
    icon = models.FileField(upload_to=path_to_variables_icons, blank=True, verbose_name='Иконка')
    image = models.ImageField(upload_to=path_to_variables_images, blank=True, verbose_name='Картинка')
    is_active = models.BooleanField(default=True, verbose_name='Активная?')
    order = models.IntegerField(default=0, blank=True, verbose_name='Порядковый номер')
    name = models.CharField(max_length=255, blank=False, verbose_name='Имя переменной')

    def __str__(self):
        return self.title if self.title else f'Переменная #{self.pk}'

    def save(self, *args, **kwargs):
        if self.pk:
            current_variable = Variable.objects.get(pk=self.pk)

            if self.icon:
                try:
                    if current_variable.icon and current_variable.icon != self.icon:
                        icon_path = Path(current_variable.icon.path)
                        if icon_path.exists():
                            icon_path.unlink()
                except Variable.DoesNotExist:
                    pass

            if self.image:
                try:
                    if current_variable.image and current_variable.image != self.image:
                        image_path = Path(current_variable.image.path)
                        if image_path.exists():
                            image_path.unlink()
                except Variable.DoesNotExist:
                    pass

        super().save(*args, **kwargs)


class Photo(models.Model):
    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['order']

    image = models.ImageField(upload_to=path_to_photos_images, blank=True, verbose_name='Картинка')
    is_active = models.BooleanField(default=True, verbose_name='Активная?')
    order = models.PositiveIntegerField(default=0, blank=True, verbose_name='Порядок')

    def __str__(self):
        return f'Слайд #{self.pk}'

    def save(self, *args, **kwargs):
        if self.pk:
            current_photo = Photo.objects.get(pk=self.pk)

            if self.image:
                try:
                    if current_photo.image and current_photo.image != self.image:
                        image_path = Path(current_photo.image.path)
                        if image_path.exists():
                            image_path.unlink()
                except Photo.DoesNotExist:
                    pass

        super().save(*args, **kwargs)


class Layout(models.Model):
    class Meta:
        verbose_name = 'Планировка'
        verbose_name_plural = 'Планировки'
        ordering = ['order']

    title = models.CharField(max_length=255, blank=True, verbose_name='Заголовок')
    image = models.ImageField(upload_to=path_to_layouts_images, blank=True, verbose_name='Картинка')
    is_active = models.BooleanField(default=True, verbose_name='Активная?')
    order = models.PositiveIntegerField(default=0, blank=True, verbose_name='Порядок')

    def __str__(self):
        return self.title if self.title else f'Планировка #{self.pk}'

    def save(self, *args, **kwargs):
        if self.pk:
            current_layout = Layout.objects.get(pk=self.pk)

            if self.image:
                try:
                    if current_layout.image and current_layout.image != self.image:
                        image_path = Path(current_layout.image.path)
                        if image_path.exists():
                            image_path.unlink()
                except Layout.DoesNotExist:
                    pass

        super().save(*args, **kwargs)


class Attraction(models.Model):
    class Meta:
        verbose_name = 'Достопримечательность'
        verbose_name_plural = 'Достопримечательности'
        ordering = ['order']

    title = models.CharField(max_length=255, blank=False, verbose_name='Заголовок')
    image = models.ImageField(upload_to=path_to_attraction_images, blank=True, verbose_name='Картинка')
    text = RichTextUploadingField(blank=True, verbose_name='Текст')
    tags = models.TextField(max_length=500, blank=True, verbose_name='Теги')
    is_active = models.BooleanField(default=True, verbose_name='Активная?')
    order = models.PositiveIntegerField(default=0, blank=True, verbose_name='Порядок')

    def __str__(self):
        return self.title

    def get_tags(self):
        if self.tags:
            return self.tags.split(',')

    def save(self, *args, **kwargs):
        if self.pk:
            current_attraction = Attraction.objects.get(pk=self.pk)

            if self.image:
                try:
                    if current_attraction.image and current_attraction.image != self.image:
                        image_path = Path(current_attraction.image.path)
                        if image_path.exists():
                            image_path.unlink()
                except Attraction.DoesNotExist:
                    pass

        super().save(*args, **kwargs)


class Card(models.Model):
    class Meta:
        verbose_name = 'Карточка'
        verbose_name_plural = 'Карточки'
        ordering = ['order']

    TYPES = [
        ('benefits', 'Идеальное месторасположение'),
        ('concept', 'Концепция «Город в городе»'),
        ('secure', 'Безопасность и приватность'),
        ('offer', 'Лучшее предложение на рынке'),
    ]

    title = models.CharField(max_length=255, blank=True, verbose_name='Заголовок')
    type = models.CharField(max_length=500, blank=False, null=False, choices=TYPES, verbose_name='Тип карточки')
    image = models.ImageField(upload_to=path_to_cards_images, blank=True, verbose_name='Картинка')
    text = models.TextField(blank=True, verbose_name='Текст')
    svg_icon = models.TextField(blank=True, verbose_name='SVG иконка')
    is_active = models.BooleanField(default=True, verbose_name='Активная?')
    order = models.PositiveIntegerField(default=0, blank=True, verbose_name='Порядок')

    def __str__(self):
        return self.title if self.title else f'Карточка #{self.pk}'

    def save(self, *args, **kwargs):
        if self.pk:
            current_card = Card.objects.get(pk=self.pk)

            if self.image:
                try:
                    if current_card.image and current_card.image != self.image:
                        image_path = Path(current_card.image.path)
                        if image_path.exists():
                            image_path.unlink()
                except Card.DoesNotExist:
                    pass

        super().save(*args, **kwargs)


class Document(models.Model):
    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['order']

    title = models.CharField(max_length=255, blank=True, verbose_name='Заголовок')
    file = models.FileField(upload_to=path_to_documents_files, blank=True, verbose_name='Файл')
    is_active = models.BooleanField(default=True, verbose_name='Активный?')
    order = models.PositiveIntegerField(default=0, blank=True, verbose_name='Порядок')

    def __str__(self):
        return self.title if self.title else f'Документ #{self.pk}'

    def save(self, *args, **kwargs):
        if self.pk:
            current_document = Document.objects.get(pk=self.pk)

            if self.file:
                try:
                    if current_document.file and current_document.file != self.file:
                        file_path = Path(current_document.file.path)
                        if file_path.exists():
                            file_path.unlink()
                except Document.DoesNotExist:
                    pass

        super().save(*args, **kwargs)


class Article(models.Model):
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = '-date',

    title = models.CharField(max_length=500, blank=False, verbose_name='Заголовок')
    date = models.DateField(auto_now_add=False, blank=False, verbose_name='Дата публикации')
    image = models.ImageField(upload_to=path_to_articles_images, blank=False, verbose_name='Картинка')
    video = models.FileField(upload_to=path_to_articles_images, blank=True, verbose_name='Видео-файл')
    text = RichTextUploadingField(blank=False, verbose_name='Текст')
    slug = models.SlugField(max_length=500, blank=False, verbose_name='Slug')
    is_active = models.BooleanField(default=True, verbose_name='Активная?')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.pk:
            current_image = Article.objects.get(pk=self.pk)

            if self.image:
                try:
                    if current_image.image and current_image.image != self.image:
                        image_path = Path(current_image.image.path)
                        if image_path.exists():
                            image_path.unlink()
                except Article.DoesNotExist:
                    pass

        super().save(*args, **kwargs)


class Application(models.Model):
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = '-created_at',

    name = models.CharField(max_length=500, blank=False, verbose_name='Имя')
    phone = models.CharField(max_length=500, blank=False, verbose_name='Телефон')
    sub = models.CharField(max_length=500, blank=False, verbose_name='Тема сообщения')
    is_processed = models.BooleanField(default=False, verbose_name='Обработанная?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отправки')

    def __str__(self):
        return f'Заявка от {self.name} ({self.phone})'
