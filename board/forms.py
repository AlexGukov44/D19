from django import forms
from .models import Posts, Comment
from django.core.exceptions import ValidationError

class PostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title','text','category',]

    ''' функция не позволяющая вписывать одинаковый заголовок и одинаковое содержание'''
    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        title = cleaned_data.get("title")
        if title == text:
            raise ValidationError("Описание не должно быть идентично названию.")

        return cleaned_data

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text_comment',]


