from django.test import TestCase
from django.urls import reverse

from services.models import Service

from .models import Project


class ProjectModelTests(TestCase):
    def test_value_display_formats_currency(self):
        project = Project(title='X', slug='x', short_description='x', value=45000000)
        self.assertEqual(project.value_display, 'KES 45,000,000')

    def test_value_display_handles_undisclosed(self):
        project = Project(title='X', slug='x', short_description='x', value=None)
        self.assertEqual(project.value_display, 'Value not disclosed')


class SeededPortfolioTests(TestCase):
    """Guards the content that ships with the site."""

    @classmethod
    def setUpTestData(cls):
        from django.core.management import call_command
        call_command('seed_site', verbosity=0)

    def test_every_cv_project_is_present(self):
        expected = {
            'mpesa-foundation-maternity-wing', 'palm-court-residence',
            'council-diplomat-residence', 'private-residence-kajiado',
            'private-residence-cheptais', 'hill-top-hotel-and-resort',
            'gitonga-resort', 'residential-renovation-chemelil',
            'kayaki-resort-sun-deck-and-pool', 'mariga-resort-cottages',
        }
        self.assertEqual(set(Project.objects.values_list('slug', flat=True)), expected)

    def test_every_project_has_a_featured_image(self):
        missing = [p.slug for p in Project.objects.all() if not p.featured_image]
        self.assertEqual(missing, [], f'projects without a featured image: {missing}')

    def test_disclosed_values_match_the_cv(self):
        values = dict(Project.objects.exclude(value=None).values_list('slug', 'value'))
        self.assertEqual(int(values['mpesa-foundation-maternity-wing']), 45000000)
        self.assertEqual(int(values['palm-court-residence']), 20000000)
        self.assertEqual(int(values['private-residence-kajiado']), 16000000)
        self.assertEqual(int(values['private-residence-cheptais']), 15500000)
        self.assertEqual(int(values['residential-renovation-chemelil']), 4500000)
        self.assertEqual(int(values['kayaki-resort-sun-deck-and-pool']), 2000000)
        # The CV discloses no value for these three.
        self.assertEqual(sum(values.values()), 103000000)

    def test_portfolio_work_carries_attribution(self):
        for project in Project.objects.exclude(slug='council-diplomat-residence'):
            with self.subTest(project=project.slug):
                self.assertTrue(project.role, f'{project.slug} has no role')

    def test_home_hero_prefers_a_completed_project(self):
        response = self.client.get(reverse('pages:home'))
        self.assertEqual(response.context['hero_project'].status, 'completed')


class ProjectViewTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            title='Resort Design', slug='resort-design', category='hospitality',
            short_description='x', full_description='x', icon='fa',
        )
        self.project = Project.objects.create(
            title='Hill Top Hotel & Resort', slug='hill-top', service=self.service,
            short_description='A hillside resort.', location='Uasin Gishu County',
            role='Design & Site Supervision', delivered_with='Eco Space Architects',
            status='in_progress', is_published=True,
        )

    def test_detail_page_shows_attribution(self):
        response = self.client.get(self.project.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Design &amp; Site Supervision')
        self.assertContains(response, 'Eco Space Architects')

    def test_unpublished_project_is_404(self):
        self.project.is_published = False
        self.project.save()

        self.assertEqual(self.client.get(self.project.get_absolute_url()).status_code, 404)

    def test_service_filter_narrows_results(self):
        other_service = Service.objects.create(
            title='Renovations', slug='renovations', category='renovation',
            short_description='x', full_description='x', icon='fa',
        )
        Project.objects.create(
            title='Chemelil Extension', slug='chemelil', service=other_service,
            short_description='x', is_published=True,
        )

        url = f"{reverse('projects:list')}?service=resort-design"
        response = self.client.get(url)

        self.assertContains(response, 'Hill Top Hotel')
        self.assertNotContains(response, 'Chemelil Extension')
