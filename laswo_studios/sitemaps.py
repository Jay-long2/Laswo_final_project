from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Post
from projects.models import Project
from services.models import Service


class StaticSitemap(Sitemap):
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return ['pages:home', 'pages:about', 'pages:contact', 'services:list', 'projects:list']

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class ProjectSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return Project.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class PostSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at


SITEMAPS = {
    'static': StaticSitemap,
    'services': ServiceSitemap,
    'projects': ProjectSitemap,
    'posts': PostSitemap,
}
