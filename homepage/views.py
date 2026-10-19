from django.http import HttpResponse


def page(title: str, content: str) -> str:
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">Коллекции</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/collections/">Коллекции</a>
                <a class="nav-link" href="/items/">Экспонаты</a>
            </div>
        </div>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    content = """
    <div class="p-5 mb-4 bg-white rounded-3 shadow-sm">
        <h1 class="display-5 fw-bold">Сервис управления личными коллекциями</h1>
        <p class="lead">
            Веб-интерфейс для каталогизации частных собраний, учета редких
            экспонатов и оценки стоимости предметов.
        </p>
        <hr class="my-4">
        <p>Перейдите в интересующий вас раздел каталога:</p>
        <a href="/collections/" class="btn btn-primary me-2">Коллекции</a>
        <a href="/items/" class="btn btn-secondary">Экспонаты</a>
    </div>
    """
    return HttpResponse(page("Главная — Сервис коллекций", content))


def page_not_found(request, exception):
    content = """
    <div class="text-center py-5">
        <h1 class="display-1 text-danger">404</h1>
        <h2 class="mb-4">Страница не найдена</h2>
        <p class="lead">Запрашиваемый адрес не существует или был перемещен.</p>
        <a href="/" class="btn btn-primary">Вернуться на главную</a>
    </div>
    """
    return HttpResponse(
        page("404 — Страница не найдена", content),
        status=404,
    )
