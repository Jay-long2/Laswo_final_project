from django.conf import settings


def company(request):
    """Make the company contact details available to every template."""
    return {'company': settings.COMPANY}
