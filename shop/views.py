from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from .models import Article, Category,ArticleImage,Coupon
from django.core.paginator import Paginator

def home_view(request):
    q = request.GET.get('q', '')

    articles = Article.objects.filter(is_active=True)

    if q:
        articles = articles.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )

    paginator = Paginator(articles, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.filter(is_active=True)

    return render(request, 'shop/home.html', {
        'page_obj': page_obj,
        'categories': categories,
    })





def article_list(request):
    articles = Article.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)

    # filtres
    category = request.GET.get('category')
    min_price = request.GET.get('min')
    max_price = request.GET.get('max')

    if category:
        articles = articles.filter(category__slug=category)

    if min_price:
        articles = articles.filter(price__gte=min_price)

    if max_price:
        articles = articles.filter(price__lte=max_price)

    return render(request, 'shop/list.html', {
        'articles': articles,
        'categories': categories,
    })


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk, is_active=True)
    images = article.images.all()
    return render(request, 'shop/article_detail.html', {
        'article': article,
        'images': images,
    })

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    articles = category.articles.filter(is_active=True)

    return render(request, 'shop/category.html', {
        'category': category,
        'articles': articles,
    })


def search_view(request):
    q = request.GET.get('q', '')
    articles = Article.objects.filter(
        Q(name__icontains=q) |
        Q(description__icontains=q),
        is_active=True
    )
    return render(request, 'shop/search.html', {
        'articles': articles,
        'query': q,
    })

def article_images(request, pk):
    article = get_object_or_404(Article, pk=pk, is_active=True)
    images = ArticleImage.objects.filter(article=article)

    return render(request, 'shop/images.html', {
        'article': article,
        'images': images,
    })

def coupon_list(request):
    now = timezone.now()

    coupons = Coupon.objects.filter(
        is_active=True
    ).filter(
        Q(valid_from__lte=now) | Q(valid_from__isnull=True),
        Q(valid_to__gte=now) | Q(valid_to__isnull=True),
    )

    return render(request, 'shop/coupons.html', {
        'coupons': coupons,
    })

