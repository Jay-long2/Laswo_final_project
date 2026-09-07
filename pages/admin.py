from django.contrib import admin

from .models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'service', 'budget_range', 'status', 'created_at']
    list_filter = ['status', 'service', 'budget_range', 'created_at']
    list_editable = ['status']
    search_fields = ['name', 'phone', 'email', 'location', 'message']
    readonly_fields = [
        'name', 'phone', 'email', 'location', 'service',
        'budget_range', 'message', 'created_at',
    ]
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Enquiry', {
            'fields': (
                'name', 'phone', 'email', 'location',
                'service', 'budget_range', 'message', 'created_at',
            )
        }),
        ('Follow-up', {'fields': ('status', 'notes')}),
    )

    def has_add_permission(self, request):
        # Enquiries only ever arrive through the public form.
        return False
