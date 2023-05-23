from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from .middleware import get_current_user
from django.db.models import Q


# Create your models here.

class Users(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    post_users = models.ForeignKey('Posts', on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.name

class Posts(models.Model):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, verbose_name='Заголовок:')
    text = models.TextField(blank=False, verbose_name='Содержание:')
    files = models.FileField()

    category = models.ForeignKey(to='Categories', on_delete=models.CASCADE, verbose_name='Категория:')


    def __str__(self):
        return f'{self.title}: {self.text[:28]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])



class Categories(models.Model):
    tanks = 'NE'
    hills = 'AR'
    dd = 'DD'
    merchants ='ME'
    guildmasters = 'GU'
    questgivers = 'QU'
    blacksmiths = 'BL'
    leatherworkers = 'LE'
    potions = 'PO'
    spell_masters = 'SP'


    TYPES = [
        (tanks, 'Танки'),
        (hills, 'Хиллы'),
        (dd, 'ДД'),
        (merchants, 'Торговцы'),
        (guildmasters, 'Гилдмастеры'),
        (questgivers, 'Квестгиверы'),
        (blacksmiths, 'Кузнецы'),
        (leatherworkers, 'Кожевники'),
        (potions, 'Зельевары'),
        (spell_masters, 'Мастера заклинаний'),

    ]

    type = models.CharField(max_length=2, choices=TYPES, default=tanks)
    title_post = models.CharField(max_length=255, blank=True)

""" Класс для принятия или удаления комментариев создателем статьи"""
class StatusComment(models.Manager):
    def get_queryset(self):
        print(get_current_user())
        return super().get_queryset().filter(Q(status=False,link_2 = get_current_user()) | Q(status=False,
                                             link_1__author=get_current_user()) | Q(status=True))

class Comment(models.Model):
    link_1 = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comment_posts')
    link_2 = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField(blank=False, verbose_name='Содержание')
    time_in_comment = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(verbose_name='рассматриваемый комментарий', default=False)
    objects = StatusComment()

    def __str__(self):
        return f'{self.text_comment[:28]}: {self.time_in_comment}'

    # def get_absolute_url(self):
    #     return reverse('post_comments', args=[str(self.id)])

