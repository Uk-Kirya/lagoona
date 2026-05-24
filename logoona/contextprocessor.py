from typing import Any
from django.http import HttpRequest

from content.models import Variable, Layout


def context_all(request: HttpRequest) -> dict[str, Any]:

    wishlist = request.session.get('wishlist', [])

    context = {
        "vars": Variable.objects.all(),
        "hero_block": Variable.objects.get(name='hero_block').text_3,
        "about": Variable.objects.get(name='about').text_3,
        "layouts_text": Variable.objects.get(name='layouts_text').text_3,
        "garant": Variable.objects.get(name='garant'),
        "phone": Variable.objects.get(name='phone').text_1,
        "location": Variable.objects.get(name='location').text_1,
        "email": Variable.objects.get(name='email').text_1,
        "instagram": Variable.objects.get(name='instagram').text_1,
        "telegram": Variable.objects.get(name='telegram').text_1,
        "whatsapp": Variable.objects.get(name='whatsapp').text_1,
        "map": Variable.objects.get(name='map').text_2,
        "policy": Variable.objects.get(name='policy').text_3,
        "wishlist": wishlist,
        "wishlist_items": Layout.objects.filter(id__in=wishlist),
    }

    return context
