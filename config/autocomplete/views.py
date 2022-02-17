from config.settings import AUTOCOMPLETE_SEARCH_FIELD
from django.shortcuts import render
from django.views import View
from django.apps import apps
from django.conf import settings
from django.http import JsonResponse


class AutocompleteView(View):
    """View responsible for handling ajax requests from the autocompleter."""

    def get(self, request, *args, **kwargs):
        """Handles autocompletion for get http requests."""
        term = request.GET.get('term')

        model = apps.get_model(settings.AUTOCOMPLETE_MODEL, None)
        search_field = getattr(settings, 'AUTOCOMPLETE_SEARCH_FIELD', None)
        order_fields = getattr(settings, 'AUTOCOMPLETE_ORDER_FIELDS', None)
        print(order_fields)

        if all((model, search_field, order_fields)):
            search = {f'{search_field}__icontains': term}
            items = model.objects.filter(**search).order_by(*order_fields)
            items = [getattr(item, search_field) for item in items]
            items_uniq = [*{*items}]
            return JsonResponse(items_uniq, safe=False)
        return JsonResponse([], safe=False)