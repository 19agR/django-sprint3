from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class PostQuerySet(models.QuerySet):
    """Кастомный QuerySet для фильтрации опубликованных постов."""

    def published(self):
        """Возвращает опубликованные посты с опубликованной категорией."""
        return self.select_related('location', 'category').filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )

    def latest_published(self, count=5):
        """
        Возвращает последние 'count' опубликованных постов,
        отсортированных по дате.
        """
        return self.published().order_by('-pub_date')[:count]


class PublishedModel(models.Model):
    """
    Абстрактная модель.

    Поля:
        - is_published: опубликован ли пост.
        - created_at: дата создания.
    """

    is_published = models.BooleanField(
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
        verbose_name='Опубликовано')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено')

    class Meta:
        abstract = True


class Category(PublishedModel):
    """
    Модель категории публикаций.

    Поля:
        - title: Заголовок категории.
        - description: Описание категории.
        - slug: Уникальный идентификатор для URL.
    """

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'),
        verbose_name='Идентификатор')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel):
    """
    Модель местоположения публикации.

    Поля:
        - name: Название места.
    """

    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(PublishedModel):
    """
    Модель публикации.

    Поля:
        - title: Заголовок публикации.
        - text: Текст публикации.
        - pub_date: Дата и время публикации.
        - author: Автор публикации.
        - location: Местоположение (необязательно).
        - category: Категория (необязательно).
    """

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'),
        verbose_name='Дата и время публикации')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации')
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Местоположение')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория')

    objects = PostQuerySet.as_manager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title
