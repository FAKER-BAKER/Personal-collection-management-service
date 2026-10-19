from django.shortcuts import render
from essence.collections import find_collection_by_id
from storage import load_categories, load_collections, load_items, load_users


def collections_list(request):
    users = load_users("data/users.json")
    cols = load_collections("data/collections.json", users)
    cats = load_categories("data/categories.json")
    items = load_items("data/items.json", cols, cats)

    for col in cols:
        col_items = [i for i in items if i.collection.id == col.id]
        setattr(col, "items_count", len(col_items))
        setattr(col, "total_value", sum(i.price for i in col_items))

    context = {
        "collections": cols,
    }
    return render(request, "collections_app/collection_list.html", context)


def collection_detail(request, collection_id: int):
    users = load_users("data/users.json")
    cols = load_collections("data/collections.json", users)
    col = find_collection_by_id(cols, collection_id)

    col_items = []
    total_val = 0.0
    if col is not None:
        cats = load_categories("data/categories.json")
        items = load_items("data/items.json", cols, cats)
        col_items = [i for i in items if i.collection.id == col.id]
        total_val = sum(i.price for i in col_items)

    context = {
        "col": col,
        "items": col_items,
        "total_val": total_val,
    }
    return render(
        request,
        "collections_app/collection_detail.html",
        context,
        status=404 if col is None else 200,
    )
