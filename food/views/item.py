from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required

from ..forms import ItemSearchForm


@require_GET
@login_required
def index_items(request: HttpRequest):
    item_search_form = ItemSearchForm(request.user, request.GET)

    return render(request, "food/items.html", {"items": item_search_form.get_items()})
