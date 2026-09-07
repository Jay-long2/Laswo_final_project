"""Seed the site with Laswo Studios' real services and project portfolio.

Project data is taken from the founder's CV. Values marked "not disclosed"
are left blank rather than invented, and roles are recorded exactly as held.

Safe to re-run: everything is matched on slug and updated in place.
"""

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from projects.models import Project, ProjectImage
from services.models import Service, ServiceFeature

SERVICES = [
    {
        'slug': 'architectural-design',
        'title': 'Architectural Design',
        'category': 'design',
        'icon': 'fa-solid fa-pen-ruler',
        'display_order': 1,
        'short_description': (
            'Concept design through to council-ready working drawings for homes, '
            'resorts and institutional buildings.'
        ),
        'full_description': (
            'We take a project from the first sketch to a full set of drawings your '
            'contractor and the county can build from.\n\n'
            'That means understanding your site and budget, developing a concept you '
            'are genuinely happy with, and then producing the architectural drawings, '
            'details and schedules needed for approval and construction. We work in '
            'ArchiCAD and AutoCAD, and present designs in 3D so you can see the '
            'building before a single stone is laid.'
        ),
        'duration': '4 - 10 weeks',
        'features': [
            ('Site analysis & brief', 'We start with your plot, your budget and how you want to live in the space.', 'fa-solid fa-map-location-dot'),
            ('Concept & 3D visuals', 'Photorealistic renders so you can see and approve the design before construction.', 'fa-solid fa-cube'),
            ('Working drawings', 'Fully dimensioned architectural drawings coordinated with structural and services detail.', 'fa-solid fa-file-lines'),
            ('Approval support', 'Drawings prepared to meet county and local authority requirements.', 'fa-solid fa-stamp'),
        ],
    },
    {
        'slug': 'design-and-build',
        'title': 'Design & Build',
        'category': 'build',
        'icon': 'fa-solid fa-trowel-bricks',
        'display_order': 2,
        'short_description': (
            'One team, one contract - from the first drawing to handover of the '
            'finished building.'
        ),
        'full_description': (
            'Design and build puts the drawing board and the site under a single point '
            'of responsibility. You deal with one team, and there is no gap between '
            'what was designed and what gets built.\n\n'
            'It is usually the fastest route to a finished building, and it makes cost '
            'control far easier because the design is tested against the budget as it '
            'develops rather than after the fact.'
        ),
        'duration': '6 - 18 months',
        'features': [
            ('Single point of contact', 'One team accountable for both the design and the construction.', 'fa-solid fa-handshake'),
            ('Costed as designed', 'The budget is tested at every design stage, not discovered at tender.', 'fa-solid fa-calculator'),
            ('Faster delivery', 'Construction can begin on early packages while later detail is finalised.', 'fa-solid fa-gauge-high'),
        ],
    },
    {
        'slug': 'construction-supervision',
        'title': 'Construction Supervision',
        'category': 'supervision',
        'icon': 'fa-solid fa-helmet-safety',
        'display_order': 3,
        'short_description': (
            'Regular site inspection and contractor coordination so the building that '
            'goes up matches the one you approved.'
        ),
        'full_description': (
            'Drawings only protect you if somebody checks the work against them. We '
            'supervise construction from foundation through to finishes - inspecting '
            'work as it happens, coordinating trades, and catching problems while they '
            'are still cheap to fix.\n\n'
            'You get straight answers about progress, quality and cost, from someone '
            'whose job is to represent your interests on site.'
        ),
        'duration': 'Duration of works',
        'features': [
            ('Scheduled site visits', 'Regular inspection at every key stage, from setting out to final finishes.', 'fa-solid fa-clipboard-check'),
            ('Quality control', 'Work checked against drawings and specification before it gets covered up.', 'fa-solid fa-magnifying-glass'),
            ('Progress reporting', 'Clear updates on where the project stands against programme and budget.', 'fa-solid fa-chart-line'),
        ],
    },
    {
        'slug': 'renovations-and-extensions',
        'title': 'Renovations & Extensions',
        'category': 'renovation',
        'icon': 'fa-solid fa-house-chimney-crack',
        'display_order': 4,
        'short_description': (
            'Extend, remodel or add a storey to an existing home - including full '
            'bungalow-to-maisonette conversions.'
        ),
        'full_description': (
            'Working with an existing building is a different discipline to starting '
            'from scratch. The structure has to be assessed before anything is added, '
            'and the new work has to read as part of the original rather than bolted on.\n\n'
            'We have taken existing bungalows up to two storeys, reworked internal '
            'layouts, and extended homes to suit growing families - designing and '
            'supervising the work through to completion.'
        ),
        'duration': '3 - 9 months',
        'features': [
            ('Structural assessment', 'We establish what the existing building can carry before designing on top of it.', 'fa-solid fa-ruler-combined'),
            ('Storey additions', 'Bungalow-to-maisonette conversions, designed and supervised end to end.', 'fa-solid fa-layer-group'),
            ('Live-in phasing', 'Where possible, work is staged so the house stays usable.', 'fa-solid fa-calendar-days'),
        ],
    },
    {
        'slug': 'resort-and-hospitality-design',
        'title': 'Resort & Hospitality Design',
        'category': 'hospitality',
        'icon': 'fa-solid fa-umbrella-beach',
        'display_order': 5,
        'short_description': (
            'Cottages, lodges, decks and pool facilities designed to sit well in the '
            'landscape and work commercially.'
        ),
        'full_description': (
            'Hospitality buildings have to do two jobs at once: give guests somewhere '
            'memorable to stay, and make commercial sense for the owner.\n\n'
            'Our hospitality work includes A-frame guest cottages on sloping sites, '
            'elevated walkways linking accommodation to central lodge and restaurant '
            'blocks, and leisure facilities such as sun decks, swimming pools and pool '
            'bars - designed around the terrain rather than flattening it.'
        ),
        'duration': '6 - 24 months',
        'features': [
            ('Site-led planning', 'Cottages and walkways laid out to follow the contours and the views.', 'fa-solid fa-mountain-sun'),
            ('Guest cottages & lodges', 'A-frame and multi-level cottage designs linked to central facilities.', 'fa-solid fa-house-chimney'),
            ('Leisure facilities', 'Sun decks, swimming pools and pool bars designed as part of the whole.', 'fa-solid fa-water-ladder'),
        ],
    },
]

# Ordered most impressive first - this is also the portfolio display order.
PROJECTS = [
    {
        'slug': 'mpesa-foundation-maternity-wing',
        'title': 'M-Pesa Foundation Maternity Wing',
        'service': 'architectural-design',
        'location': 'Likuyani, Kakamega County',
        'client_name': 'M-Pesa Foundation',
        'year_label': '2025 - 2026',
        'status': 'in_progress',
        'role': 'Design & Site Supervision',
        'delivered_with': 'Eco Space Architects',
        'value': 45000000,
        'is_featured': True,
        'short_description': (
            'An institutional maternity facility commissioned by the M-Pesa Foundation - '
            'the largest project in our founder\'s portfolio to date.'
        ),
        'full_description': (
            'A maternity wing commissioned by the M-Pesa Foundation in Likuyani, '
            'Kakamega County. At KES 45 million it is the largest project in our '
            'founder\'s portfolio, and the one that best demonstrates the standard of '
            'coordination institutional work demands.\n\n'
            'The commission covered full architectural design and construction '
            'supervision from foundation through to roofing.'
        ),
        'challenge': (
            'A healthcare building funded by a major foundation carries requirements a '
            'private home does not - clinical layout standards, strict compliance, and '
            'a donor expecting the work to be accounted for at every stage.'
        ),
        'solution': (
            'Design was developed against healthcare planning requirements from the '
            'outset, and construction was supervised on site from foundation through '
            'to roofing so that work was checked against drawings as it happened.'
        ),
    },
    {
        'slug': 'palm-court-residence',
        'title': 'Palm Court Residence',
        'service': 'architectural-design',
        'location': 'Kahawa Sukari, Nairobi County',
        'status': 'completed',
        'role': 'Design & Site Supervision',
        'delivered_with': 'Eco Space Architects',
        'value': 20000000,
        'is_featured': True,
        'short_description': (
            'A high-end contemporary residential villa in Nairobi, taken from full '
            'architectural design through to construction supervision.'
        ),
        'full_description': (
            'A contemporary villa in Kahawa Sukari, Nairobi, delivered from concept '
            'design through to completion on site.\n\n'
            'The brief called for generous, well-lit living space with a clear '
            'separation between the family areas and the guest and entertaining wing.'
        ),
    },
    {
        'slug': 'council-diplomat-residence',
        'title': 'Council Diplomat Residence',
        'service': 'architectural-design',
        'client_name': 'Joseph Ogola',
        'status': 'proposed',
        'role': 'Architectural Design & Working Drawings',
        'is_featured': True,
        'short_description': (
            'A proposed two-storey residence with a stone facade, arched glazing and a '
            'lake view terrace - shown here in design visualisation.'
        ),
        'full_description': (
            'A proposed residential development designed around a formal entrance '
            'court and a lake view terrace.\n\n'
            'The ground floor holds the lounge, dining, kitchen and pantry alongside a '
            'self-contained guest wing, with the master suite and further bedrooms '
            'above. The elevation pairs a dressed stone facade with tall arched glazing '
            'and deep eaves to shade the interior.\n\n'
            'A full set of working drawings has been prepared at 1:100, coordinated '
            'with structural and services detail and set out to meet local authority '
            'requirements.'
        ),
    },
    {
        'slug': 'private-residence-kajiado',
        'title': 'Private Residence, Kajiado',
        'service': 'design-and-build',
        'location': 'Kajiado County',
        'status': 'completed',
        'role': 'Design & Site Supervision',
        'delivered_with': 'Eco Space Architects',
        'value': 16000000,
        'short_description': (
            'A residential villa delivered under a design-and-build arrangement, from '
            'concept design through to construction.'
        ),
        'full_description': (
            'A family villa in Kajiado County delivered as a single design-and-build '
            'commission, with design and construction held under one point of '
            'responsibility from concept through to completion.'
        ),
    },
    {
        'slug': 'private-residence-cheptais',
        'title': 'Private Residence, Cheptais',
        'service': 'architectural-design',
        'location': 'Cheptais, Bungoma County',
        'year_label': '2024 - 2025',
        'status': 'completed',
        'role': 'Design & Site Supervision',
        'delivered_with': 'Eco Space Architects',
        'value': 15500000,
        'short_description': (
            'A two-storey residential villa in Bungoma County, with full architectural '
            'design and on-site construction supervision.'
        ),
        'full_description': (
            'A two-storey family villa in Cheptais, Bungoma County. The commission '
            'covered the full architectural design and supervision of construction on '
            'site through to completion.'
        ),
    },
    {
        'slug': 'hill-top-hotel-and-resort',
        'title': 'Hill Top Hotel & Resort',
        'service': 'resort-and-hospitality-design',
        'location': 'Uasin Gishu County',
        'status': 'in_progress',
        'role': 'Design & Site Supervision',
        'delivered_with': 'Eco Space Architects',
        'value': None,
        'short_description': (
            'A hillside resort of A-frame guest cottages linked by elevated walkways to '
            'a central lodge and restaurant block. Currently under construction.'
        ),
        'full_description': (
            'A resort development on a sloping site in Uasin Gishu County, comprising '
            'multiple A-frame guest cottages connected by elevated walkways to a '
            'central lodge and restaurant block.\n\n'
            'The layout follows the contours of the hillside so that each cottage keeps '
            'its outlook and privacy, and the walkways cross the slope rather than '
            'cutting into it. The project is currently under construction.'
        ),
    },
    {
        'slug': 'gitonga-resort',
        'title': 'Gitonga Resort',
        'service': 'resort-and-hospitality-design',
        'location': 'Mbiuni, Machakos County',
        'status': 'completed',
        'role': 'Design & Build',
        'delivered_with': 'Eco Space Architects',
        'value': None,
        'short_description': (
            'A hillside resort of multi-level A-frame cottages, delivered under a '
            'design-and-build arrangement.'
        ),
        'full_description': (
            'A resort development at Mbiuni in Machakos County made up of multi-level '
            'A-frame cottages stepped into the hillside, delivered as a design-and-build '
            'commission.'
        ),
    },
    {
        'slug': 'residential-renovation-chemelil',
        'title': 'Residential Renovation & Extension, Chemelil',
        'service': 'renovations-and-extensions',
        'location': 'Chemelil, Kisumu County',
        'status': 'completed',
        'role': 'Design & Site Supervision',
        'delivered_with': 'Eco Space Architects',
        'value': 4500000,
        'short_description': (
            'An existing bungalow renovated and extended upwards into a full two-storey '
            'family residence.'
        ),
        'full_description': (
            'The client wanted more space without leaving a home and a location the '
            'family was settled in.\n\n'
            'Rather than build new, the existing bungalow was assessed, reworked and '
            'extended upwards into a two-storey residence - keeping the original '
            'structure and the address, and adding the space the family needed.'
        ),
        'challenge': (
            'Adding a storey to a house that was never designed to carry one, while the '
            'family kept living in it.'
        ),
        'solution': (
            'The existing structure was assessed before any design work began, and the '
            'extension was designed and phased around what the building could carry.'
        ),
    },
    {
        'slug': 'kayaki-resort-sun-deck-and-pool',
        'title': 'Kayaki Resort - Sun Deck, Pool & Pool Bar',
        'service': 'resort-and-hospitality-design',
        'location': 'Bondo, Siaya County',
        'status': 'completed',
        'role': 'Design & Site Supervision',
        'delivered_with': 'Eco Space Architects',
        'value': 2000000,
        'short_description': (
            'A leisure facility comprising an elevated sun deck, swimming pool and pool '
            'bar for a lakeside resort.'
        ),
        'full_description': (
            'A leisure addition to an existing resort at Bondo in Siaya County, made up '
            'of an elevated sun deck, a swimming pool and a pool bar designed to work '
            'together as a single guest area.'
        ),
    },
    {
        'slug': 'mariga-resort-cottages',
        'title': 'Mariga Resort Cottages',
        'service': 'resort-and-hospitality-design',
        'location': 'Mariga, Baringo County',
        'status': 'proposed',
        'role': 'Design Architect',
        'delivered_with': 'Eco Space Architects',
        'value': None,
        'short_description': (
            'Proposed A-frame resort cottages set within a natural landscape in Baringo '
            'County.'
        ),
        'full_description': (
            'Concept and design development for a set of proposed A-frame resort '
            'cottages in Mariga, Baringo County, placed within the existing landscape '
            'so that the natural setting carries the character of the scheme.'
        ),
    },
]


# Images follow a slug convention so they need no per-project wiring:
#   media/projects/featured/<slug>.jpg      the card and hero image
#   media/projects/gallery/<slug>-NN.jpg    gallery, in numeric order
# Only the captions need naming.
GALLERY_CAPTIONS = {
    'council-diplomat-residence-02': 'Rear elevation and garden terrace',
    'council-diplomat-residence-03': 'Side elevation showing the entrance court',

    'palm-court-residence-02': 'Structural frame and roofing under way',
    'palm-court-residence-03': 'Roof and gable detail nearing completion',
    'palm-court-residence-04': 'Finishing works in progress on the front elevation',
    'palm-court-residence-05': 'Entrance colonnade detail',
    'palm-court-residence-06': 'Verandah columns and eaves under construction',

    'mpesa-foundation-maternity-wing-02': 'Roofing works over the main ward block',
    'private-residence-cheptais-02': 'Nearing completion, with scaffolding still in place',
    'private-residence-kajiado-02': 'Stonework and gable detail',
    'residential-renovation-chemelil-02': 'The original bungalow, before work began',
    'kayaki-resort-sun-deck-and-pool-02': 'Elevated sun deck and access stair under construction',
    'mariga-resort-cottages-02': 'Proposed A-frame cottage in its landscape setting',
    'gitonga-resort-02': 'Multi-level A-frame cottages stepped into the hillside',

    'hill-top-hotel-and-resort-02': 'Cottage structure and roof framing on site',
    'hill-top-hotel-and-resort-03': 'A completed cottage shell on its stone base',
    'hill-top-hotel-and-resort-04': 'Roof cladding complete on one of the cottages',
    'hill-top-hotel-and-resort-05': 'Gable glazing seen from the lake side',
    'hill-top-hotel-and-resort-06': 'Interior view out through the gable glazing',
}


class Command(BaseCommand):
    help = "Seed services and the project portfolio from Laswo Studios' real records."

    def add_arguments(self, parser):
        parser.add_argument(
            '--if-empty',
            action='store_true',
            help=(
                'Only seed when no projects exist yet. Use this on deploy so the '
                'first boot is populated but later admin edits are never overwritten.'
            ),
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.verbosity = options['verbosity']

        if options['if_empty'] and Project.objects.exists():
            self._log(
                f'Skipping seed: {Project.objects.count()} projects already exist.'
            )
            return

        services = {}

        for data in SERVICES:
            features = data.pop('features', [])
            slug = data.pop('slug')
            service, created = Service.objects.update_or_create(slug=slug, defaults=data)
            services[slug] = service
            data['slug'] = slug
            data['features'] = features

            service.features.all().delete()
            for title, description, icon in features:
                ServiceFeature.objects.create(
                    service=service, title=title, description=description, icon=icon
                )

            self._log(f"  {'created' if created else 'updated'} service: {service.title}")

        for order, data in enumerate(PROJECTS, start=1):
            data = dict(data)
            slug = data.pop('slug')
            service_slug = data.pop('service', None)

            data['service'] = services.get(service_slug)
            data['display_order'] = order

            project, created = Project.objects.update_or_create(slug=slug, defaults=data)
            images = self._attach_images(project)

            self._log(
                f"  {'created' if created else 'updated'} project: {project.title} "
                f"({images} image{'' if images == 1 else 's'})"
            )

        # Retire anything left over from the old sample data rather than
        # deleting it, so nothing added by hand is lost.
        stale = Service.objects.exclude(slug__in=services).filter(is_active=True)
        for service in stale:
            service.is_active = False
            service.save(update_fields=['is_active'])
            self._log(f'  retired stale service: {service.title}', self.style.WARNING)

        self._log(
            f'\nSeeded {Service.objects.count()} services and '
            f'{Project.objects.count()} projects.',
            self.style.SUCCESS,
        )

    def _log(self, message, style=None):
        if self.verbosity:
            self.stdout.write(style(message) if style else message)

    def _attach_images(self, project):
        """Wire up images already sitting in MEDIA_ROOT, by slug convention.

        Files are referenced in place rather than re-saved, so re-running the
        command does not pile up duplicates like image_1.jpg, image_2.jpg.
        """
        media = Path(settings.MEDIA_ROOT)
        count = 0

        featured = f'projects/featured/{project.slug}.jpg'
        if (media / featured).exists():
            project.featured_image.name = featured
            project.save(update_fields=['featured_image'])
            count += 1
        else:
            self._log(
                f'    no featured image for {project.slug} - using placeholder',
                self.style.WARNING,
            )

        project.images.all().delete()
        gallery = sorted((media / 'projects' / 'gallery').glob(f'{project.slug}-*.jpg'))
        for order, path in enumerate(gallery, start=1):
            image = ProjectImage(
                project=project,
                caption=GALLERY_CAPTIONS.get(path.stem, ''),
                display_order=order,
            )
            image.image.name = f'projects/gallery/{path.name}'
            image.save()
            count += 1

        return count
