from django.db import models
from django.utils import timezone

from .constants import AMOUNT_POSTS_MAIN_PAGE


class PostQuerySet(models.QuerySet):
    """Кастомный QuerySet для фильтрации опубликованных постов."""

    def published(self):
        """Возвращает опубликованные посты с опубликованной категорией."""
        return self.select_related('location', 'category', 'author').filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )

    def latest_published(self):
        """
        Возвращает опубликованные посты, отсортированные по дате.

        Количество постов берется из константы AMOUNT_POSTS_MAIN_PAGE.
        Сортировка по дате от новых к старым работает по умолчанию.
        """
        return self.published()[:AMOUNT_POSTS_MAIN_PAGE]
