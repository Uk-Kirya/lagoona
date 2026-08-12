from django.urls import path

from .views import (
    HomePageView,
    PolicyPageView,
    BlogPageView,
    ArticlePageView,
    ApplicationView,
    WishlistView,
    agreed_to_policy,
    sitemap,
)

app_name = 'content'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('agreed-to-policy/', agreed_to_policy, name='agreed_to_policy'),
    path('policy/', PolicyPageView.as_view(), name='policy'),
    path('blog/', BlogPageView.as_view(), name='blog'),
    path('send-message/', ApplicationView.as_view(), name='send-message'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('blog/<slug:slug>', ArticlePageView.as_view(), name='article'),
    path('sitemap.xml', sitemap, name='sitemap'),
]
