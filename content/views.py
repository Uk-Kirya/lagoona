from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages

from content.models import Photo, Layout, Attraction, Card, Document, Article, Application, HomeSEOBlock
from logoona import settings


class HomePageView(View):
    def get(self, request):
        context = {
            "photos": Photo.objects.filter(is_active=True),
            "layouts": Layout.objects.filter(is_active=True),
            "attractions": Attraction.objects.filter(is_active=True),
            "cards": Card.objects.filter(is_active=True),
            "concept_cards": Card.objects.filter(is_active=True, type='concept'),
            "documents": Document.objects.filter(is_active=True),
            "articles": Article.objects.filter(is_active=True)[:3],
            "home_seo": HomeSEOBlock.objects.filter(is_active=True).first(),
        }
        return render(request=request, template_name='home.html', context=context)


class PolicyPageView(TemplateView):
    template_name = 'policy.html'


class BlogPageView(View):
    def get(self, request):
        articles = Article.objects.filter(is_active=True)

        paginator = Paginator(articles, 12)
        page_number = request.GET.get('page', 1)

        try:
            articles = paginator.page(page_number)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context = {
            "paginator": paginator,
            "articles": articles,
        }
        if articles.number > 1:
            context['canonical_url'] = f'{settings.SITE_URL}{request.path}?page={articles.number}'
        return render(request=request, template_name='blog.html', context=context)


class ArticlePageView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article.objects.filter(is_active=True), slug=slug)
        articles = Article.objects.filter(is_active=True).exclude(pk=article.pk)[:2]
        meta_description = Truncator(strip_tags(article.text)).chars(160)

        context = {
            "article": article,
            "articles": articles,
            "meta_description": meta_description or 'Новости и полезная информация от Lagoona Resort & Spa.',
        }

        return render(request, 'article.html', context=context)


class ApplicationView(View):
    def post(self, request):

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')

        message = render_to_string('message.html', {
            'name': name,
            'phone': phone,
            'subject': subject,
        })

        try:
            application = Application.objects.create(
                name=name,
                phone=phone,
                sub=subject,
            )
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ['udarnik.kirill@gmail.com'],
                html_message=message,
                fail_silently=False
            )
        except Exception as e:
            print("EMAIL ERROR:", e)

        messages.success(request, 'Ваша заявка успешно отправлена!')
        return redirect(request.META.get('HTTP_REFERER', '/'))


class WishlistView(View):
    def post(self, request):
        pk = int(request.POST.get('pk'))

        wishlist = request.session.get('wishlist', [])

        if pk in wishlist:
            wishlist.remove(pk)
        else:
            wishlist.append(pk)

        request.session['wishlist'] = wishlist

        return redirect(request.META.get('HTTP_REFERER', '/'))


def agreed_to_policy(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        request.session['agreed_to_policy'] = True
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error'}, status=400)


def sitemap(request: HttpRequest) -> HttpResponse:
    articles = Article.objects.filter(is_active=True)
    latest_article = articles.first()
    content = render_to_string(
        'sitemap.xml',
        {
            'site_url': settings.SITE_URL,
            'articles': articles,
            'latest_article': latest_article,
        },
    )
    return HttpResponse(content, content_type='application/xml; charset=utf-8')
