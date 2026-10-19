from django.shortcuts import render
from essence.items import find_item_by_id
from storage import load_categories, load_collections, load_items, load_users


def items_list(request):
    users = load_users("data/users.json")
    cols = load_collections("data/collections.json", users)
    cats = load_categories("data/categories.json")
    items = load_items("data/items.json", cols, cats)

    context = {
        "items": items,
    }
    return render(request, "items_app/item_list.html", context)


def item_detail(request, item_id: int):
    users = load_users("data/users.json")
    cols = load_collections("data/collections.json", users)
    cats = load_categories("data/categories.json")
    items = load_items("data/items.json", cols, cats)
    it = find_item_by_id(items, item_id)

    context = {
        "it": it,
    }
    return render(
        request,
        "items_app/item_detail.html",
        context,
        status=404 if it is None else 200,
    )
