from .services import get_site_content


def site_content(request):
    return {"site_content": get_site_content()}
