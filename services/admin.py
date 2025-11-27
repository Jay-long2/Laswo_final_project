from django.contrib import admin
from .models import Service, ServiceFeature, ServiceImage

# Register your models here.
class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1

class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'display_order', 'is_active', 'starting_price']
    list_filter = ['category', 'is_active']
    search_fields = ['title', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ServiceFeatureInline, ServiceImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'short_description', 'full_description')
        }),
        ('Media & Display', {
            'fields': ('icon', 'featured_image', 'display_order', 'is_active')
        }),
        ('Pricing & Details', {
            'fields': ('starting_price', 'duration')
        }),
    )

@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'service', 'icon']
    list_filter = ['service']
    search_fields = ['title', 'service__title']

@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ['service', 'caption', 'display_order']
    list_filter = ['service']