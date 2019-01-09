from .models import Service


def services(request):
    return {
        'services_slugs': Service.objects.values_list('slug', flat=True).order_by('id')
    }
