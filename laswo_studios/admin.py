from django.contrib import admin
from django.db.models import Count
from blog.models import Post, Comment
from projects.models import Project
from services.models import Service

class LaswoAdminSite(admin.AdminSite):
    site_header = "Laswo Studios Administration"
    site_title = "Laswo Studios Admin"
    index_title = "🏗️ Construction Business Dashboard"
    
    def index(self, request, extra_context=None):
        # Add custom stats to the admin index
        extra_context = extra_context or {}
        
        # Get counts for quick stats
        extra_context['blog_count'] = Post.objects.filter(status='published').count()
        extra_context['project_count'] = Project.objects.filter(is_published=True).count()
        extra_context['service_count'] = Service.objects.filter(is_active=True).count()
        extra_context['comment_count'] = Comment.objects.filter(is_approved=False).count()
        
        return super().index(request, extra_context)

# Replace the default admin site
admin_site = LaswoAdminSite(name='laswo_admin')

# Register all models with our custom admin site
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

# Register your app models
from services.models import Service, ServiceFeature, ServiceImage
from projects.models import Project, ProjectImage, ProjectCategory
from blog.models import Post, Category, Tag, Comment, NewsletterSubscriber

admin_site.register(Service)
admin_site.register(ServiceFeature)
admin_site.register(ServiceImage)
admin_site.register(Project)
admin_site.register(ProjectImage)
admin_site.register(ProjectCategory)
admin_site.register(Post)
admin_site.register(Category)
admin_site.register(Tag)
admin_site.register(Comment)
admin_site.register(NewsletterSubscriber)