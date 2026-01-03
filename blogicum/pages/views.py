from django.shortcuts import render


def about(request):
    """
    Страница «О проекте».

    Отображает информацию о проекте «Блогикум».
    """
    return render(request, 'pages/about.html')


def rules(request):
    """
    Страница «Правила».

    Отображает правила использования проекта.
    """
    return render(request, 'pages/rules.html')
