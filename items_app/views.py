from django.http import HttpResponse
from essence.items import find_item_by_id
from homepage.views import page
from storage import load_categories, load_collections, load_items, load_users


def items_list(request):
    users = load_users("data/users.json")
    cols = load_collections("data/collections.json", users)
    cats = load_categories("data/categories.json")
    items = load_items("data/items.json", cols, cats)

    rows = ""
    for it in items:
        badge = "bg-warning text-dark" if it.check_rarity() == "Раритет" else "bg-secondary"
        rows += f"""
        <tr>
            <td>{it.id}</td>
            <td><a href="/items/{it.id}/" class="fw-bold">{it.name}</a></td>
            <td>{it.category.name}</td>
            <td>{it.year}</td>
            <td><span class="badge {badge}">{it.check_rarity()}</span></td>
            <td>{it.price:,.2f} руб.</td>
            <td><a href="/collections/{it.collection.id}/">{it.collection.name}</a></td>
        </tr>
        """

    content = f"""
    <h1 class="mb-4">Реестр предметов и экспонатов</h1>
    <div class="table-responsive shadow-sm">
        <table class="table table-striped table-hover bg-white mb-0">
            <thead class="table-dark">
                <tr>
                    <th>ID</th>
                    <th>Название</th>
                    <th>Категория</th>
                    <th>Год</th>
                    <th>Редкость</th>
                    <th>Стоимость</th>
                    <th>Коллекция</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """
    return HttpResponse(page("Список экспонатов", content))


def item_detail(request, item_id: int):
    users = load_users("data/users.json")
    cols = load_collections("data/collections.json", users)
    cats = load_categories("data/categories.json")
    items = load_items("data/items.json", cols, cats)
    it = find_item_by_id(items, item_id)

    if it is None:
        content = """
        <div class="alert alert-danger" role="alert">
            <h4 class="alert-heading">Экспонат не найден!</h4>
            <p>Предмет с указанным идентификатором отсутствует в реестре.</p>
            <hr>
            <a href="/items/" class="btn btn-outline-danger">К списку предметов</a>
        </div>
        """
        return HttpResponse(page("Предмет не найден", content), status=404)

    rarity_badge = "bg-danger" if it.check_rarity() == "Раритет" else "bg-info text-dark"
    expensive_badge = "bg-success" if it.is_expensive(10000.0) else "bg-secondary"
    expensive_text = (
        "Высокая ценность (>= 10,000 руб.)"
        if it.is_expensive(10000.0)
        else "Обычная ценность"
    )

    content = f"""
    <div class="card shadow-sm">
        <div class="card-header bg-dark text-white">
            <h4 class="my-0">Экспонат ID #{it.id}: {it.name}</h4>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Категория:</strong> {it.category.name}</p>
                    <p><strong>Год выпуска:</strong> {it.year} г.</p>
                    <p><strong>Состояние:</strong> {it.condition}</p>
                    <p><strong>Оценочная стоимость:</strong> <span class="fs-5 fw-bold text-primary">{it.price:,.2f} руб.</span></p>
                </div>
                <div class="col-md-6">
                    <p><strong>Владелец:</strong> {it.collection.user.username}</p>
                    <p><strong>Входит в коллекцию:</strong> <a href="/collections/{it.collection.id}/">{it.collection.name}</a></p>
                    <p><strong>Редкость:</strong> <span class="badge {rarity_badge}">{it.check_rarity()}</span></p>
                    <p><strong>Финансовый статус:</strong> <span class="badge {expensive_badge}">{expensive_text}</span></p>
                </div>
            </div>
            <hr>
            <a href="/items/" class="btn btn-outline-secondary">← Вернуться к реестру предметов</a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Экспонат: {it.name}", content), status=200)
