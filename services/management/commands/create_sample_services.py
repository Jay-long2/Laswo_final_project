from django.core.management.base import BaseCommand
from services.models import Service, ServiceFeature

class Command(BaseCommand):
    help = 'Create sample services for development'
    
    def handle(self, *args, **options):
        # House Renovations Service
        renovation, created = Service.objects.get_or_create(
            title="Complete House Renovations",
            slug="house-renovations",
            defaults={
                'category': 'renovation',
                'short_description': 'Transform your entire home with our comprehensive renovation services.',
                'full_description': """Our complete house renovation service transforms your living space from outdated to extraordinary. We handle everything from initial design consultation to final finishing touches.

We specialize in:
• Whole-home transformations
• Kitchen and bathroom remodels
• Room additions and expansions
• Structural modifications
• Interior design coordination

Our team works with you to understand your vision and bring it to life with quality craftsmanship and attention to detail.""",
                'icon': 'fas fa-home',
                'starting_price': 25000,
                'duration': '4-8 weeks',
                'display_order': 1,
            }
        )
        
        if created:
            # Add features for renovations
            features = [
                {'title': 'Kitchen Remodeling', 'icon': 'fas fa-utensils', 'description': 'Modern kitchen designs with quality cabinets and countertops'},
                {'title': 'Bathroom Renovations', 'icon': 'fas fa-bath', 'description': 'Luxury bathroom upgrades with modern fixtures'},
                {'title': 'Room Additions', 'icon': 'fas fa-plus-square', 'description': 'Expand your living space with new room construction'},
                {'title': 'Interior Design', 'icon': 'fas fa-palette', 'description': 'Professional design consultation and implementation'},
            ]
            
            for feature_data in features:
                ServiceFeature.objects.create(service=renovation, **feature_data)
        
        # Landscaping Service
        landscaping, created = Service.objects.get_or_create(
            title="Professional Landscaping",
            slug="landscaping",
            defaults={
                'category': 'landscaping',
                'short_description': 'Create stunning outdoor living spaces with our expert landscaping services.',
                'full_description': """Transform your outdoor space into a beautiful, functional area perfect for entertainment and relaxation. Our landscaping services combine artistic design with practical functionality.

Services include:
• Custom garden design and installation
• Patio and deck construction
• Irrigation system installation
• Outdoor lighting
• Landscape maintenance

We use quality materials and sustainable practices to create outdoor spaces that enhance your property's value and beauty.""",
                'icon': 'fas fa-tree',
                'starting_price': 5000,
                'duration': '2-4 weeks',
                'display_order': 2,
            }
        )
        
        if created:
            features = [
                {'title': 'Garden Design', 'icon': 'fas fa-seedling', 'description': 'Beautiful garden layouts with seasonal plants'},
                {'title': 'Patio Construction', 'icon': 'fas fa-th-large', 'description': 'Durable and attractive patio spaces'},
                {'title': 'Irrigation Systems', 'icon': 'fas fa-tint', 'description': 'Efficient watering systems for your landscape'},
                {'title': 'Outdoor Lighting', 'icon': 'fas fa-lightbulb', 'description': 'Ambient lighting for safety and beauty'},
            ]
            
            for feature_data in features:
                ServiceFeature.objects.create(service=landscaping, **feature_data)
        
        # Roofing Service
        roofing, created = Service.objects.get_or_create(
            title="Roofing Solutions",
            slug="roofing",
            defaults={
                'category': 'roofing',
                'short_description': 'Professional roofing services including repairs, replacements, and new installations.',
                'full_description': """Protect your home with our professional roofing services. We provide comprehensive roofing solutions using the highest quality materials and workmanship.

Our roofing services include:
• Complete roof replacements
• Emergency roof repairs
• Roof inspections and maintenance
• Gutter installation and repair
• Skylight installation

We work with various roofing materials including asphalt shingles, metal roofing, tile, and flat roof systems to meet your specific needs and budget.""",
                'icon': 'fas fa-hard-hat',
                'starting_price': 8000,
                'duration': '1-3 weeks',
                'display_order': 3,
            }
        )
        
        if created:
            features = [
                {'title': 'Roof Repairs', 'icon': 'fas fa-tools', 'description': 'Quick and reliable repair services'},
                {'title': 'Roof Replacement', 'icon': 'fas fa-sync', 'description': 'Complete roof system replacement'},
                {'title': 'Emergency Services', 'icon': 'fas fa-exclamation-triangle', 'description': '24/7 emergency roofing services'},
                {'title': 'Roof Inspections', 'icon': 'fas fa-search', 'description': 'Comprehensive roof assessment and reports'},
            ]
            
            for feature_data in features:
                ServiceFeature.objects.create(service=roofing, **feature_data)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample services!')
        )