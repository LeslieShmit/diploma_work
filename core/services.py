from .models import SiteContent

def get_site_content():
    return SiteContent.objects.filter(pk=1).first()