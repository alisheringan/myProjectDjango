from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Comment


@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    """Отправляет email при создании нового комментария"""
    if created and instance.is_approved:
        try:
            subject = f'Новый комментарий к посту: {instance.post.title}'
            message = f'''
Новый комментарий на вашем сайте!

Пост: {instance.post.title}
Автор: {instance.author_name}
Тема: {instance.subject}
Дата: {instance.created_date.strftime("%d.%m.%Y %H:%M")}

Текст комментария:
{instance.text}

Ссылка на пост: {settings.SITE_URL}/post/{instance.post.id}/
            '''

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['momunaliev.alisher@gmail.com'],  # Ваш email
                fail_silently=False,
            )
            print(f"✅ Email отправлен о комментарии #{instance.id}")
        except Exception as e:
            print(f"❌ Ошибка отправки email: {str(e)}")