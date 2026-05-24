from django.urls import path

from .views import (
    HomePageView,
    PolicyPageView,
    BlogPageView,
    ArticlePageView,
    ApplicationView,
    WishlistView
)

app_name = 'content'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('policy/', PolicyPageView.as_view(), name='policy'),
    path('blog/', BlogPageView.as_view(), name='blog'),
    path('send-message/', ApplicationView.as_view(), name='send-message'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('blog/<slug:slug>', ArticlePageView.as_view(), name='article'),
]
