from django.db import models
from django.urls import reverse

class Service(models.Model):
    SERVICE_CATEGORIES = [
        ('renovation', 'House Renovations'),
        ('landscaping', 'Landscaping'),
        ('roofing', 'Roofing Solutions'),
        ('construction', 'New Construction'),
        ('other', 'Other Services'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=SERVICE_CATEGORIES)
    short_description = models.TextField(max_length=200)
    full_description = models.TextField()
    icon = models.CharField(max_length=100, help_text="FontAwesome icon class")
    featured_image = models.ImageField(upload_to='services/', blank=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Service details
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration = models.CharField(max_length=100, blank=True, help_text="e.g., 2-4 weeks")
    
    class Meta:
        ordering = ['display_order', 'title']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'slug': self.slug})

class ServiceFeature(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, help_text="FontAwesome icon class")
    
    def __str__(self):
        return f"{self.service.title} - {self.title}"

class ServiceImage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='services/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['display_order']
    
    def __str__(self):
        return f"{self.service.title} - {self.caption or 'Image'}"