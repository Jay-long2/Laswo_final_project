"""URL configuration for laswo_studios."""

from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve

from .sitemaps import SITEMAPS

admin.site.site_header = 'Laswo Studios Administration'
admin.site.site_title = 'Laswo Studios Admin'
admin.site.index_title = 'Business Dashboard'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('services/', include('services.urls')),
    path('projects/', include('projects.urls')),
    path('blog/', include('blog.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': SITEMAPS}, name='django.contrib.sitemaps.views.sitemap'),
    path(
        'robots.txt',
        TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),
        name='robots',
    ),
]

# Portfolio images are committed to the repo and served by the app in both
# modes. Move to object storage (S3/Cloudinary) before relying on uploads made
# through the admin, since Render's free disk is wiped on every deploy.
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
