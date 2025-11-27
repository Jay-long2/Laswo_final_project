from django.shortcuts import render, get_object_or_404
from .models import Service

#create your views here.
def service_list(request):
    services = Service.objects.filter(is_active=True).order_by('display_order')
    
    # Group services by category
    services_by_category = {}
    for service in services:
        if service.category not in services_by_category:
            services_by_category[service.category] = []
        services_by_category[service.category].append(service)
    
    context = {
        'services': services,
        'services_by_category': services_by_category,
    }
    return render(request, 'services/list.html', context)

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    context = {
        'service': service,
        'features': service.features.all(),
        'images': service.images.all(),
    }
    return render(request, 'services/detail.html', context)