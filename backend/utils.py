from django.db.models import Count

from .models import *

menu = [{'profile': "Профиль", 'url_name': 'profile'},
        {'strategy': "Торговые стратегии", 'url_name': 'strategy'},
        {'community': "Сообщество", 'url_name': 'community'},
]


class DataMixin:
    paginate_by = 2

    def get_user_context(self, **kwargs):
        context = kwargs
        prof = Profile.objects.annotate(Count('user'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['prof'] = prof
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

