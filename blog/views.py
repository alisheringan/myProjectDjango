from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.contrib import messages

from .models import Post, Comment, Category
from .forms import CommentForm


# Главная страница с кешированием
@cache_page(60 * 5)
@vary_on_cookie
def index(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_date')

    search_query = request.GET.get('search', '')
    if search_query:
        posts = posts.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))

    category_filter = request.GET.get('category', '')
    if category_filter:
        posts = posts.filter(category_id=category_filter)

    date_filter = request.GET.get('date_filter', '')
    if date_filter == 'week':
        posts = posts.filter(created_date__gte=timezone.now() - timezone.timedelta(days=7))
    elif date_filter == 'month':
        posts = posts.filter(created_date__gte=timezone.now() - timezone.timedelta(days=30))

    categories = Category.objects.all()

    return render(request, 'blog/index.html', {
        'posts': posts,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_filter,
        'selected_date_filter': date_filter,
    })


def about(request):
    return render(request, 'blog/about.html')


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')

        if name and email and message_text:
            subject = f"Новое сообщение от {name}"
            full_message = f"Имя: {name}\nEmail: {email}\n\nСообщение:\n{message_text}"
            try:
                send_mail(subject, full_message, settings.DEFAULT_FROM_EMAIL, ['momunaliev.alisher@gmail.com'], fail_silently=False)
                messages.success(request, "Сообщение успешно отправлено!")
            except Exception as e:
                messages.error(request, f"Ошибка при отправке email: {e}")
            return redirect('contact')
        else:
            messages.error(request, "Пожалуйста, заполните все поля формы.")

    return render(request, 'blog/contact.html')


def test_email(request):
    """Тестовая функция отправки email для проверки"""
    try:
        send_mail(
            'Тестовое письмо',
            'Это тестовое письмо для проверки.',
            settings.DEFAULT_FROM_EMAIL,
            ['momunaliev.alisher@gmail.com'],
            fail_silently=False,
        )
        return HttpResponse('✅ Письмо отправлено!')
    except Exception as e:
        return HttpResponse(f'❌ Ошибка: {str(e)}')


def hide_comment(request, comment_id):
    if request.method == 'POST' and request.user.is_authenticated and request.user.is_staff:
        comment = get_object_or_404(Comment, id=comment_id)
        comment.is_approved = False
        comment.save()
    return redirect(request.META.get('HTTP_REFERER', 'index'))


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    user_posts = Post.objects.filter(author=request.user)
    user_comments = Comment.objects.filter(author_name=request.user.username)
    return render(request, 'registration/profile.html', {
        'user_posts': user_posts,
        'user_comments': user_comments,
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, is_published=True)
    post.views_count += 1
    post.save(update_fields=['views_count'])

    comments = Comment.objects.filter(post=post, is_approved=True).order_by('-created_date')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.author_name = request.user.username
            comment.save()
            send_comment_email(comment, post, request)
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})


def send_comment_email(comment, post, request):
    try:
        subject = f'[Мой Блог] Новый комментарий: "{post.title}"'
        post_url = request.build_absolute_uri(f'/post/{post.id}/')
        message = f'''
Новый комментарий на вашем блоге!

Пост: {post.title}
Автор: {comment.author_name}
Тема: {comment.subject}
Дата: {comment.created_date.strftime("%d.%m.%Y %H:%M")}

Текст комментария:
{comment.text}

Ссылка на пост: {post_url}
        '''
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['momunaliev.alisher@gmail.com'], fail_silently=False)
    except Exception as e:
        print(f"❌ Ошибка отправки email: {str(e)}")
