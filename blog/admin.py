from django.contrib import admin
from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # ✅ Отображаемые поля в списке + кастомное поле
    list_display = ['name', 'description_short', 'posts_count']

    # ✅ Скрыть неиспользуемые поля (пока все используются)
    exclude = []

    # ✅ Поля только для чтения (кастомное поле)
    readonly_fields = ['posts_count']

    # ✅ Поле поиска (уже было)
    search_fields = ['name', 'description']

    # ✅ СПОСОБЫ ФИЛЬТРАЦИИ - ДОБАВИЛИ
    list_filter = ['created_date']  # Нужно добавить created_date в модель Category

    # 🔧 КАСТОМНЫЕ МЕТОДЫ
    def description_short(self, obj):
        """Сокращенное описание для списка"""
        if obj.description:
            return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
        return "—"

    description_short.short_description = 'Описание'

    def posts_count(self, obj):
        """Количество постов в категории (только чтение)"""
        return obj.post_set.count()

    posts_count.short_description = 'Кол-во постов'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # ✅ Отображаемые поля в списке + кастомные поля
    list_display = ['title', 'author', 'category', 'created_date_short', 'is_published', 'comments_count']

    # ✅ СКРЫТЬ НЕИСПОЛЬЗУЕМЫЕ ПОЛЯ - ДОБАВИЛИ
    exclude = ['published_date']  # Скрываем если не используем

    # ✅ ПОЛЯ ТОЛЬКО ДЛЯ ЧТЕНИЯ - ДОБАВИЛИ
    readonly_fields = ['created_date', 'comments_count']

    # ✅ Поле поиска (расширили)
    search_fields = ['title', 'content', 'author__username', 'category__name']

    # ✅ Способы фильтрации (уже были)
    list_filter = ['is_published', 'category', 'created_date', 'author']
    date_hierarchy = 'created_date'

    # 🔧 Группировка полей (уже была) + добавили секцию только для чтения
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content', 'image')
        }),
        ('Дополнительная информация', {
            'fields': ('author', 'category', 'is_published')
        }),
        ('Статистика (только чтение)', {
            'fields': ('created_date', 'comments_count'),
            'classes': ('collapse',)  # Сворачиваемая секция
        }),
    )

    # 🔧 КАСТОМНЫЕ МЕТОДЫ
    def created_date_short(self, obj):
        """Короткая дата создания"""
        return obj.created_date.strftime("%d.%m.%Y %H:%M")

    created_date_short.short_description = 'Дата создания'

    def comments_count(self, obj):
        """Количество комментариев (только чтение)"""
        return obj.comment_set.count()

    comments_count.short_description = 'Комментарии'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # ✅ Отображаемые поля в списке + кастомные поля
    list_display = ['author_name', 'subject_short', 'post_title', 'created_date_short', 'is_approved']

    # ✅ Скрыть неиспользуемые поля (пока все используются)
    exclude = []

    # ✅ ПОЛЯ ТОЛЬКО ДЛЯ ЧТЕНИЯ - ДОБАВИЛИ
    readonly_fields = ['created_date', 'post_title']

    # ✅ Поле поиска (уже было)
    search_fields = ['author_name', 'subject', 'text', 'post__title']

    # ✅ Способы фильтрации (уже были)
    list_filter = ['is_approved', 'created_date', 'post']

    # ✅ Редактируемые поля (уже было)
    list_editable = ['is_approved']

    # ✅ Действия (уже были)
    actions = ['approve_comments', 'disapprove_comments']

    # 🔧 КАСТОМНЫЕ МЕТОДЫ
    def subject_short(self, obj):
        """Сокращенная тема"""
        return obj.subject[:30] + "..." if len(obj.subject) > 30 else obj.subject

    subject_short.short_description = 'Тема'

    def post_title(self, obj):
        """Название поста (только чтение)"""
        return obj.post.title

    post_title.short_description = 'Пост'

    def created_date_short(self, obj):
        """Короткая дата создания"""
        return obj.created_date.strftime("%d.%m.%Y %H:%M")

    created_date_short.short_description = 'Дата'

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    approve_comments.short_description = "Одобрить выбранные комментарии"

    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)

    disapprove_comments.short_description = "Снять с публикации выбранные комментарии"