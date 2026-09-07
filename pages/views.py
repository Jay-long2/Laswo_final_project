import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from blog.models import Post
from projects.models import Project
from services.models import Service

from .forms import EnquiryForm

logger = logging.getLogger(__name__)


def _notify(enquiry):
    """Email the team about a new enquiry. Never block the visitor on failure."""
    lines = [
        f'Name:     {enquiry.name}',
        f'Phone:    {enquiry.phone}',
        f'Email:    {enquiry.email or "-"}',
        f'Location: {enquiry.location or "-"}',
        f'Service:  {enquiry.service or "-"}',
        f'Budget:   {enquiry.get_budget_range_display() or "-"}',
        '',
        enquiry.message,
    ]
    try:
        send_mail(
            subject=f'New enquiry from {enquiry.name}',
            message='\n'.join(lines),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ENQUIRY_NOTIFY_EMAIL],
            fail_silently=False,
        )
    except Exception:
        logger.exception('Could not send enquiry notification for #%s', enquiry.pk)


def home(request):
    featured = list(
        Project.objects.filter(is_published=True, is_featured=True)
        .select_related('service')[:3]
    )

    # The hero wants a finished building rather than a live building site,
    # so prefer a completed project before falling back to anything with a photo.
    with_image = [p for p in featured if p.featured_image]
    hero = next((p for p in with_image if p.status == 'completed'), None)
    if hero is None:
        hero = next(iter(with_image), None)
    if hero is None:
        hero = Project.objects.filter(is_published=True).exclude(featured_image='').first()

    context = {
        'services': Service.objects.filter(is_active=True)[:5],
        'hero_project': hero,
        'featured_projects': featured,
        'recent_posts': Post.objects.filter(status='published').select_related('category')[:3],
    }
    return render(request, 'pages/home.html', context)


def about(request):
    return render(request, 'pages/about.html', {
        'project_count': Project.objects.filter(is_published=True).count(),
    })


def contact(request):
    """Render the enquiry form and handle its submission."""
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            _notify(enquiry)
            messages.success(
                request,
                'Thank you. Your enquiry has reached us and we will be in touch shortly.',
            )
            return redirect('pages:contact')
        messages.error(request, 'Please correct the highlighted fields and try again.')
    else:
        form = EnquiryForm(initial={'service': request.GET.get('service') or None})

    return render(request, 'pages/contact.html', {'form': form})
