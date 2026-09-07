from django.db import models
from django.urls import reverse

from services.models import Service


class Project(models.Model):
    PROJECT_STATUS = [
        ('completed', 'Completed'),
        ('in_progress', 'Under Construction'),
        ('proposed', 'Proposed / In Design'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    service = models.ForeignKey(
        Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects'
    )

    location = models.CharField(max_length=200, blank=True, help_text='e.g. Likuyani, Kakamega County')
    client_name = models.CharField(max_length=200, blank=True)
    year_label = models.CharField(
        max_length=50, blank=True, help_text='Free text, e.g. "2024-2025" or "Ongoing"'
    )

    short_description = models.TextField(max_length=300)
    full_description = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to='projects/featured/', blank=True)

    status = models.CharField(max_length=20, choices=PROJECT_STATUS, default='completed')

    # Honest attribution: the role our founder held, and who the work was
    # delivered with. Both surface on the public project page.
    role = models.CharField(
        max_length=200, blank=True, help_text='e.g. Design & Site Supervision'
    )
    delivered_with = models.CharField(
        max_length=200, blank=True, help_text='Practice the project was delivered with, if any'
    )

    value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Project value in KES. Leave blank if not disclosed.',
    )

    challenge = models.TextField(blank=True, help_text="What was the client's challenge?")
    solution = models.TextField(blank=True, help_text='How was it solved?')
    result = models.TextField(blank=True, help_text='What was the outcome?')

    client_testimonial = models.TextField(blank=True)
    client_company = models.CharField(max_length=200, blank=True)

    display_order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': self.slug})

    @property
    def value_display(self):
        if self.value is None:
            return 'Value not disclosed'
        return f'KES {self.value:,.0f}'


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.project.title} - {self.caption or 'Image'}"
