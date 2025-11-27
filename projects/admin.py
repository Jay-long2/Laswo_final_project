from django.contrib import admin
from .models import Project, ProjectImage, ProjectCategory

# Register your models here.
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'service', 'status', 'completion_date', 'is_featured', 'is_published']
    list_filter = ['status', 'service', 'is_featured', 'is_published']
    search_fields = ['title', 'client_name', 'location']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'service', 'client_name', 'location')
        }),
        ('Content', {
            'fields': ('short_description', 'full_description', 'featured_image')
        }),
        ('Project Details', {
            'fields': ('challenge', 'solution', 'result', 'client_testimonial', 'client_company')
        }),
        ('Timeline & Budget', {
            'fields': ('start_date', 'completion_date', 'budget', 'status')
        }),
        ('Display Options', {
            'fields': ('display_order', 'is_featured', 'is_published')
        }),
    )

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'display_order']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ['project', 'caption', 'is_primary', 'display_order']
    list_filter = ['project']