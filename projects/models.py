from django.db import models
from django.urls import reverse
from services.models import Service

# Create your models here.
class Project(models.Model):
    PROJECT_STATUS = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('upcoming', 'Upcoming'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='projects')
    client_name = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    
    short_description = models.TextField(max_length=200)
    full_description = models.TextField()
    
    featured_image = models.ImageField(upload_to='projects/featured/')
    status = models.CharField(max_length=20, choices=PROJECT_STATUS, default='completed')
    
    start_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Project details
    challenge = models.TextField(blank=True, help_text="What was the client's challenge?")
    solution = models.TextField(blank=True, help_text="How did we solve it?")
    result = models.TextField(blank=True, help_text="What was the outcome?")
    
    client_testimonial = models.TextField(blank=True)
    client_company = models.CharField(max_length=200, blank=True)
    
    display_order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-completion_date', 'display_order', 'title']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': self.slug})
    
    @property
    def duration(self):
        if self.start_date and self.completion_date:
            months = (self.completion_date.year - self.start_date.year) * 12 + (self.completion_date.month - self.start_date.month)
            return f"{months} month{'s' if months != 1 else ''}"
        return "Varies"

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['display_order']
    
    def __str__(self):
        return f"{self.project.title} - {self.caption or 'Image'}"

class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = "Project categories"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('projects:category', kwargs={'slug': self.slug})