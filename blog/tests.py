from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Category, Comment, NewsletterSubscriber, Post


class BlogViewTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user('nicholas', password='x')
        self.category = Category.objects.create(name='Construction Tips', slug='construction-tips')
        self.post = Post.objects.create(
            title='Choosing a roof', slug='choosing-a-roof', author=self.author,
            category=self.category, excerpt='On roofs.', content='word ' * 400,
            status='published', published_at=timezone.now(),
        )

    def test_detail_increments_view_count_without_touching_updated_at(self):
        before = Post.objects.get(pk=self.post.pk).updated_at

        self.client.get(self.post.get_absolute_url())

        refreshed = Post.objects.get(pk=self.post.pk)
        self.assertEqual(refreshed.view_count, 1)
        self.assertEqual(refreshed.updated_at, before)

    def test_category_url_redirects_to_filtered_list(self):
        response = self.client.get(
            reverse('blog:category', args=[self.category.slug]), follow=True
        )

        self.assertRedirects(response, f"{reverse('blog:list')}?category=construction-tips")
        self.assertContains(response, 'Choosing a roof')

    def test_tag_url_for_unknown_tag_is_404(self):
        self.assertEqual(
            self.client.get(reverse('blog:tag', args=['nope'])).status_code, 404
        )

    def test_draft_posts_are_hidden(self):
        self.post.status = 'draft'
        self.post.save()

        self.assertEqual(self.client.get(self.post.get_absolute_url()).status_code, 404)
        self.assertNotContains(self.client.get(reverse('blog:list')), 'Choosing a roof')

    def test_search_filters_posts(self):
        response = self.client.get(f"{reverse('blog:list')}?q=zzzznomatch")
        self.assertNotContains(response, 'Choosing a roof')
        # The search box must never render the string "None".
        self.assertNotContains(response, 'value="None"')

    def test_empty_search_box_is_blank(self):
        self.assertNotContains(self.client.get(reverse('blog:list')), 'value="None"')


class CommentTests(TestCase):
    def setUp(self):
        author = User.objects.create_user('n', password='x')
        category = Category.objects.create(name='Tips', slug='tips')
        self.post = Post.objects.create(
            title='T', slug='t', author=author, category=category,
            excerpt='e', content='c', status='published', published_at=timezone.now(),
        )
        self.url = reverse('blog:add_comment', args=[self.post.slug])

    def test_comment_is_saved_unapproved(self):
        self.client.post(self.url, {
            'name': 'Peter', 'email': 'p@example.com', 'content': 'Useful, thanks.',
        })

        comment = Comment.objects.get()
        self.assertEqual(comment.name, 'Peter')
        self.assertFalse(comment.is_approved)

    def test_unapproved_comments_are_not_shown(self):
        Comment.objects.create(
            post=self.post, name='Spam', email='s@e.com', content='Buy cheap things',
        )

        self.assertNotContains(self.client.get(self.post.get_absolute_url()), 'Buy cheap things')

    def test_honeypot_blocks_comment_spam(self):
        self.client.post(self.url, {
            'name': 'Bot', 'email': 'b@e.com', 'content': 'spam', 'website': 'http://spam',
        })

        self.assertEqual(Comment.objects.count(), 0)


class NewsletterTests(TestCase):
    def test_subscribe_never_redirects_to_referer(self):
        """The old implementation trusted HTTP_REFERER - an open redirect."""
        response = self.client.post(
            reverse('blog:newsletter_subscribe'),
            {'email': 'reader@example.com'},
            HTTP_REFERER='https://evil.example.com/phish',
        )

        self.assertRedirects(response, reverse('blog:list'))
        self.assertTrue(NewsletterSubscriber.objects.filter(email='reader@example.com').exists())
