from .models import SiteContent


def get_site_content():
    """Функция гарантирует, что данные будут браться только из первого экземпляра класса Site Content"""
    return SiteContent.objects.filter(pk=1).first()
