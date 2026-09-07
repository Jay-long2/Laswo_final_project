from django.db import models


class Enquiry(models.Model):
    """A project enquiry submitted through the site."""

    BUDGET_RANGES = [
        ('under_2m', 'Under KES 2M'),
        ('2m_5m', 'KES 2M - 5M'),
        ('5m_15m', 'KES 5M - 15M'),
        ('15m_50m', 'KES 15M - 50M'),
        ('over_50m', 'Over KES 50M'),
        ('unsure', 'Not sure yet'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('quoted', 'Quoted'),
        ('won', 'Won'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30)
    location = models.CharField(
        max_length=120, blank=True, help_text='Where the project is located'
    )
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enquiries',
    )
    budget_range = models.CharField(max_length=20, choices=BUDGET_RANGES, blank=True)
    message = models.TextField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True, help_text='Internal follow-up notes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Enquiries'

    def __str__(self):
        return f'{self.name} - {self.created_at:%d %b %Y}'
