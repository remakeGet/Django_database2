from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    articles = Article.objects.all()
    ordering = '-published_at'
    articles = articles.order_by(ordering)
    context = {'object_list':articles,
               'ordering':ordering}

    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    

    return render(request, template, context)
