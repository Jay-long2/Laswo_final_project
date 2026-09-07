from django.shortcuts import get_object_or_404, render

from services.models import Service

from .models import Project


def project_list(request):
    projects = Project.objects.filter(is_published=True).select_related('service')

    service_filter = request.GET.get('service')
    status_filter = request.GET.get('status')

    if service_filter:
        projects = projects.filter(service__slug=service_filter)
    if status_filter:
        projects = projects.filter(status=status_filter)

    context = {
        'projects': projects,
        'services': Service.objects.filter(is_active=True),
        'statuses': Project.PROJECT_STATUS,
        'active_service': service_filter or '',
        'active_status': status_filter or '',
    }
    return render(request, 'projects/list.html', context)


def project_detail(request, slug):
    project = get_object_or_404(
        Project.objects.select_related('service'), slug=slug, is_published=True
    )

    related = Project.objects.filter(is_published=True).exclude(pk=project.pk)
    if project.service_id:
        related = related.filter(service_id=project.service_id)

    context = {
        'project': project,
        'images': project.images.all(),
        'related_projects': related[:3],
    }
    return render(request, 'projects/detail.html', context)
