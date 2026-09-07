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
