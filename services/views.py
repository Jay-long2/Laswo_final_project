from django.shortcuts import get_object_or_404, render

from .models import Service


def service_list(request):
    return render(request, 'services/list.html', {
        'services': Service.objects.filter(is_active=True).prefetch_related('features'),
    })


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)

    context = {
        'service': service,
        'features': service.features.all(),
        'images': service.images.all(),
        'other_services': Service.objects.filter(is_active=True).exclude(pk=service.pk),
    }
    return render(request, 'services/detail.html', context)
