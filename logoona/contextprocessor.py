from typing import Any
from django.conf import settings
from django.http import HttpRequest
from django.templatetags.static import static

from content.models import Variable, Layout


def context_all(request: HttpRequest) -> dict[str, Any]:

    wishlist = request.session.get('wishlist', [])

    variables = {
        variable.name: variable
        for variable in Variable.objects.filter(is_active=True)
    }

    def get_variable(name: str) -> Variable | None:
        return variables.get(name)

    context = {
        "vars": variables.values(),
        "hero_block": getattr(get_variable('hero_block'), 'text_3', ''),
        "about": getattr(get_variable('about'), 'text_3', ''),
        "layouts_text": getattr(get_variable('layouts_text'), 'text_3', ''),
        "garant": get_variable('garant'),
        "phone": getattr(get_variable('phone'), 'text_1', ''),
        "location": getattr(get_variable('location'), 'text_1', ''),
        "email": getattr(get_variable('email'), 'text_1', ''),
        "instagram": getattr(get_variable('instagram'), 'text_1', ''),
        "telegram": getattr(get_variable('telegram'), 'text_1', ''),
        "whatsapp": getattr(get_variable('whatsapp'), 'text_1', ''),
        "map": getattr(get_variable('map'), 'text_2', ''),
        "policy": getattr(get_variable('policy'), 'text_3', ''),
        "wishlist": wishlist,
        "wishlist_items": Layout.objects.filter(id__in=wishlist),
        "genplan": getattr(get_variable('genplan'), 'image', None),
        "agreed_to_policy": request.session.get('agreed_to_policy', False),
        "site_url": settings.SITE_URL,
        "canonical_url": f"{settings.SITE_URL}{request.path}",
        "seo_logo": f"{settings.SITE_URL}{static('img/Logo.svg')}",
        "seo_default_image": f"{settings.SITE_URL}{static('img/img1.png')}",
    }

    return context
