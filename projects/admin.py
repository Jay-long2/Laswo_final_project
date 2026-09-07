from django.contrib import admin

from .models import Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'service', 'location', 'status', 'is_featured', 'is_published']
    list_filter = ['status', 'service', 'is_featured', 'is_published']
    list_editable = ['is_featured', 'is_published']
    search_fields = ['title', 'location', 'client_name']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'service', 'location', 'client_name', 'year_label')
        }),
        ('Content', {
            'fields': ('short_description', 'full_description', 'featured_image')
        }),
        ('Attribution & Value', {
            'fields': ('role', 'delivered_with', 'value', 'status'),
            'description': 'Be accurate here - this is what tells visitors what we actually did.',
        }),
        ('Case Study', {
            'fields': ('challenge', 'solution', 'result', 'client_testimonial', 'client_company'),
            'classes': ('collapse',),
        }),
        ('Display Options', {'fields': ('display_order', 'is_featured', 'is_published')}),
    )


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ['project', 'caption', 'display_order']
    list_filter = ['project']
