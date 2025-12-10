from django.test import TestCase, Client
from django.core import mail
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment, Category

from django.conf import settings

if not hasattr(settings, 'DEFAULT_FROM_EMAIL'):
    settings.DEFAULT_FROM_EMAIL = 'no-reply@example.com'
if not hasattr(settings, 'SITE_URL'):
    settings.SITE_URL = 'http://localhost:8000'


class EmailTest(TestCase):
    def test_send_email(self):
        """Тест отправки email через Django"""
        result = send_mail(
            subject='Тест отправки email',
            message='Это тестовое сообщение из Django!',
            from_email='momunaliev.alisher@gmail.com',
            recipient_list=['momunaliev.alisher@gmail.com'],
            fail_silently=False,
        )

        # Проверяем, что отправлено 1 письмо
        self.assertEqual(result, 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Тест отправки email')
        self.assertIn('Это тестовое сообщение', mail.outbox[0].body)


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='postuser', password='12345')
        self.category = Category.objects.create(name="Тестовая категория")
        self.post = Post.objects.create(
            title="Тестовый пост",
            content="Тестовое содержание",
            is_published=True,
            category=self.category,
            author=self.user
        )

    def test_post_str(self):
        self.assertEqual(str(self.post), "Тестовый пост")

    def test_post_fields(self):
        self.assertEqual(self.post.content, "Тестовое содержание")
        self.assertTrue(self.post.is_published)
        self.assertEqual(self.post.category.name, "Тестовая категория")
        self.assertEqual(self.post.author.username, "postuser")


class CommentFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='commentuser', password='12345')
        self.category = Category.objects.create(name="Тест")
        self.post = Post.objects.create(
            title="Пост для комментариев",
            content="Содержание поста",
            is_published=True,
            category=self.category,
            author=self.user
        )

    def test_comment_form_valid(self):
        data = {
            'author_name': 'Тестовый пользователь',
            'subject': 'Тема комментария',
            'text': 'Текст комментария'
        }
        comment = Comment(post=self.post, **data)
        comment.save()
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().author_name, 'Тестовый пользователь')


from django.test import TestCase, override_settings
from django.core.cache.backends.dummy import DummyCache

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
class IndexViewTest(TestCase):
    def setUp(self):
        ...

        self.client = Client()
        self.user = User.objects.create_user(username='indexuser', password='12345')
        self.category = Category.objects.create(name="Категория 1")
        self.post = Post.objects.create(
            title="Главный пост",
            content="Контент главного поста",
            is_published=True,
            category=self.category,
            author=self.user
        )

    def test_index_view_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'blog/index.html')


class ContactViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_get(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/contact.html')

    def test_contact_post_valid(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Тест',
            'email': 'test@example.com',
            'message': 'Сообщение тест'
        })
        # После успешной отправки — редирект
        self.assertEqual(response.status_code, 302)


class AuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='authuser', password='12345')

    def test_login(self):
        login = self.client.login(username='authuser', password='12345')
        self.assertTrue(login)

    def test_profile_view(self):
        self.client.login(username='authuser', password='12345')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/profile.html')
