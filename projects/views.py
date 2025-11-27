from django.shortcuts import render, get_object_or_404
from .models import Project, ProjectCategory

# Create your views here.
def project_list(request):
    projects = Project.objects.filter(is_published=True).select_related('service')
    categories = ProjectCategory.objects.all()
    
    # Get filter parameters
    service_filter = request.GET.get('service')
    category_filter = request.GET.get('category')
    status_filter = request.GET.get('status')
    
    if service_filter:
        projects = projects.filter(service__slug=service_filter)
    if category_filter:
        projects = projects.filter(service__category=category_filter)
    if status_filter:
        projects = projects.filter(status=status_filter)
    
    featured_projects = projects.filter(is_featured=True)
    
    context = {
        'projects': projects,
        'featured_projects': featured_projects,
        'categories': categories,
        'active_filters': {
            'service': service_filter,
            'category': category_filter,
            'status': status_filter,
        }
    }
    return render(request, 'projects/list.html', context)

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_published=True)
    
    # Get related projects (same service)
    related_projects = Project.objects.filter(
        service=project.service,
        is_published=True
    ).exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'images': project.images.all(),
        'related_projects': related_projects,
    }
    return render(request, 'projects/detail.html', context)

def project_category(request, slug):
    category = get_object_or_404(ProjectCategory, slug=slug)
    projects = Project.objects.filter(
        service__category=category.slug,
        is_published=True
    )
    
    context = {
        'category': category,
        'projects': projects,
    }
    return render(request, 'projects/category.html', context)