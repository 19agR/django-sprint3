from django.shortcuts import get_object_or_404, render

from .models import Category, Post


def index(request):
    """
    Главная страница блога.

    Отображает список всех публикаций в обратном
    хронологическом порядке.
    """
    post_list = Post.objects.latest_published()
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """
    Страница отдельной публикации.

    Args:
        request: HTTP-запрос пользователя.
        post_id (int): Идентификатор публикации.

    Raises:
        Http404: Если публикация с указанным id не найдена.
    """
    post = get_object_or_404(
        Post.objects.published(),
        pk=post_id
    )
    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """
    Страница публикаций по категории.

    Args:
        request: HTTP-запрос пользователя.
        category_slug (str): Название категории.
    """
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = Post.objects.published().filter(category=category)
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)
