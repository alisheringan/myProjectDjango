from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    # ✅ ДОБАВИЛИ ДЛЯ ФИЛЬТРАЦИИ В АДМИНКЕ
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    published_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name='Изображение')
    # ✅ ДОБАВИЛИ ДЛЯ ПОЛЯ ТОЛЬКО ДЛЯ ЧТЕНИЯ
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    author_name = models.CharField(max_length=100, verbose_name='Имя автора')
    subject = models.CharField(max_length=200, verbose_name='Тема комментария')
    text = models.TextField(verbose_name='Текст комментария')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    is_approved = models.BooleanField(default=True, verbose_name='Одобрен')

    def __str__(self):
        return f"Комментарий от {self.author_name} к посту '{self.post.title}'"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
