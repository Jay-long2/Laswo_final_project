from django.core import mail
from django.test import TestCase
from django.urls import reverse

from projects.models import Project
from services.models import Service

from .models import Enquiry


class PublicPageTests(TestCase):
    """Every public page should return 200 with no content in the database."""

    def test_core_pages_load(self):
        for name in ['pages:home', 'pages:about', 'pages:contact',
                     'services:list', 'projects:list', 'blog:list']:
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_robots_and_sitemap(self):
        robots = self.client.get('/robots.txt')
        self.assertEqual(robots.status_code, 200)
        self.assertIn('Disallow: /admin/', robots.content.decode())
        self.assertEqual(self.client.get('/sitemap.xml').status_code, 200)

    def test_missing_page_returns_404(self):
        self.assertEqual(self.client.get('/no-such-page/').status_code, 404)


class EnquiryFormTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            title='Architectural Design', slug='architectural-design',
            category='design', short_description='x', full_description='x', icon='fa',
        )
        self.url = reverse('pages:contact')
        self.valid = {
            'name': 'Jane Wanjiru',
            'phone': '0722000000',
            'email': 'jane@example.com',
            'location': 'Kitale',
            'service': self.service.pk,
            'budget_range': '5m_15m',
            'message': 'Four bedroom maisonette on a 50x100 plot.',
            'website': '',
        }

    def test_valid_submission_is_saved_and_notified(self):
        response = self.client.post(self.url, self.valid, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Enquiry.objects.count(), 1)

        enquiry = Enquiry.objects.get()
        self.assertEqual(enquiry.name, 'Jane Wanjiru')
        self.assertEqual(enquiry.service, self.service)
        self.assertEqual(enquiry.status, 'new')

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Jane Wanjiru', mail.outbox[0].subject)
        self.assertContains(response, 'Thank you')

    def test_missing_required_fields_redisplays_form(self):
        response = self.client.post(self.url, {'name': '', 'message': '', 'website': ''})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Enquiry.objects.count(), 0)
        self.assertTrue(response.context['form'].errors)

    def test_honeypot_blocks_bots(self):
        payload = dict(self.valid, website='http://spam.example.com')
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Enquiry.objects.count(), 0)

    def test_contact_requires_a_way_to_reply(self):
        payload = dict(self.valid, phone='', email='')
        self.client.post(self.url, payload)

        self.assertEqual(Enquiry.objects.count(), 0)

    def test_service_can_be_preselected_from_query_string(self):
        response = self.client.get(f'{self.url}?service={self.service.pk}')

        self.assertEqual(response.context['form'].initial['service'], str(self.service.pk))


class HomePageContentTests(TestCase):
    def test_featured_projects_appear_on_home(self):
        service = Service.objects.create(
            title='Design', slug='design', category='design',
            short_description='x', full_description='x', icon='fa',
        )
        Project.objects.create(
            title='M-Pesa Foundation Maternity Wing',
            slug='mpesa-maternity', service=service,
            short_description='An institutional healthcare facility.',
            is_featured=True, is_published=True, value=45000000,
        )

        response = self.client.get(reverse('pages:home'))

        self.assertContains(response, 'M-Pesa Foundation Maternity Wing')
        self.assertContains(response, 'KES 45,000,000')

    def test_unpublished_projects_are_hidden(self):
        Project.objects.create(
            title='Secret Project', slug='secret',
            short_description='x', is_featured=True, is_published=False,
        )

        response = self.client.get(reverse('projects:list'))

        self.assertNotContains(response, 'Secret Project')
