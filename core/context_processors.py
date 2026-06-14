from .services import get_site_content


def site_content(request):
    """Процессор для получения данных из модели SitContent и размещении ее в шаблонах"""
    return {"site_content": get_site_content()}
