from django.http import HttpResponse
from essence.collections import find_collection_by_id
from homepage.views import page
from storage import load_categories, load_collections, load_items, load_users


def collections_list(request):
    users = load_users("data/users.json")
    cols = load_collections("data/collections.json", users)
    cats = load_categories("data/categories.json")
    items = load_items("data/items.json", cols, cats)

    items_html = ""
    for col in cols:
        col_items = [i for i in items if i.collection.id == col.id]
        total_val = sum(i.price for i in col_items)
        items_html += f"""
        <li class="list-group-item d-flex justify-content-between align-items-center">
            <div>
                <a href="/collections/{col.id}/" class="fw-bold text-decoration-none">
                    {col.name}
                </a>
                <div class="text-muted small">Владелец: {col.user.username} | {col.description}</div>
            </div>
            <span class="badge bg-primary rounded-pill">
                {len(col_items)} предм. ({total_val:,.2f} руб.)
            </span>
        </li>
        """

    content = f"""
    <h1 class="mb-4">Личные коллекции</h1>
    <ul class="list-group shadow-sm">{items_html}</ul>
    """
    return HttpResponse(page("Каталог коллекций", content))


def collection_detail(request, collection_id: int):
    users = load_users("data/users.json")
    cols = load_collections("data/collections.json", users)
    col = find_collection_by_id(cols, collection_id)

    if col is None:
        content = """
        <div class="alert alert-danger" role="alert">
            <h4 class="alert-heading">Коллекция не найдена!</h4>
            <p>Запрошенная коллекция отсутствует в системе.</p>
            <hr>
            <a href="/collections/" class="btn btn-outline-danger">К списку коллекций</a>
        </div>
        """
        return HttpResponse(page("Коллекция не найдена", content), status=404)

    cats = load_categories("data/categories.json")
    items = load_items("data/items.json", cols, cats)
    col_items = [i for i in items if i.collection.id == col.id]
    total_val = sum(i.price for i in col_items)

    rows = ""
    for it in col_items:
        rows += f"""
        <tr>
            <td>{it.id}</td>
            <td><a href="/items/{it.id}/">{it.name}</a></td>
            <td>{it.year}</td>
            <td><span class="badge bg-info text-dark">{it.check_rarity()}</span></td>
            <td>{it.price:,.2f} руб.</td>
        </tr>
        """

    content = f"""
    <div class="card mb-4 shadow-sm">
        <div class="card-body">
            <h2 class="card-title">{col.name}</h2>
            <p class="card-text text-muted">{col.description}</p>
            <p><strong>Владелец:</strong> {col.user.username} ({col.user.email})</p>
            <p><strong>Оценочная стоимость собрания:</strong> {total_val:,.2f} руб.</p>
            <a href="/collections/" class="btn btn-outline-secondary">← Все коллекции</a>
        </div>
    </div>
    <h3>Экспонаты коллекции</h3>
    <table class="table table-hover table-bordered bg-white shadow-sm">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>Название</th>
                <th>Год</th>
                <th>Редкость</th>
                <th>Цена</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
    """
    return HttpResponse(page(f"Коллекция: {col.name}", content), status=200)
