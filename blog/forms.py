from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'subject', 'text']
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя',
                'maxlength': '100'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тема комментария',
                'maxlength': '200'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш комментарий...',
                'rows': 4,
                'maxlength': '1000'
            }),
        }
        labels = {
            'author_name': 'Имя',
            'subject': 'Тема',
            'text': 'Комментарий',
        }

    # --- ВАЛИДАЦИЯ ---

    def clean_author_name(self):
        value = self.cleaned_data.get('author_name', '')
        if not value.strip():
            raise forms.ValidationError("Поле 'Имя' не может быть пустым.")
        return value

    def clean_subject(self):
        value = self.cleaned_data.get('subject', '')
        if not value.strip():
            raise forms.ValidationError("Поле 'Тема' не может быть пустым.")
        if len(value) < 5:
            raise forms.ValidationError("Тема должна содержать минимум 5 символов.")
        return value

    def clean_text(self):
        value = self.cleaned_data.get('text', '')
        if not value.strip():
            raise forms.ValidationError("Поле 'Комментарий' не может быть пустым.")
        if len(value) < 10:
            raise forms.ValidationError("Комментарий должен содержать минимум 10 символов.")
        return value
