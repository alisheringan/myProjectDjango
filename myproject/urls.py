from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from blog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Главные страницы
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),

    # Посты и комментарии
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('comment/<int:comment_id>/hide/', views.hide_comment, name='hide_comment'),

    # Аутентификация
    path('accounts/register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    # Тестовый email
    path('test-email/', views.test_email, name='test_email'),

    # Интернационализация
    path('i18n/', include('django.conf.urls.i18n')),

    # Админка
    path('admin/', admin.site.urls),
]

# Подключение медиа-файлов только в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
