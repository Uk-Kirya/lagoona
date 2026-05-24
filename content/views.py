from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages

from content.models import Photo, Layout, Attraction, Card, Document, Article, Application
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
        return render(request=request, template_name='blog.html', context=context)


class ArticlePageView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        articles = Article.objects.filter(is_active=True).exclude(pk=article.pk)[:2]

        context = {
            "article": article,
            "articles": articles,
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
