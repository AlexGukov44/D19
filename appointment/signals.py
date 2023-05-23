# from django.db.models.signals import post_save
# from django.dispatch import receiver  # импортируем нужный декоратор
# from django.core.mail import mail_managers
#
# from .board.models import Comment
#
#
# # в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
# @receiver(post_save, sender=Comment)
# def notify_managers_comments(sender, instance, created, **kwargs):
#     if created:
#         subject = f' Написал комментарий {instance.link_2} {instance.time_in_comment("%d %m %Y")} '
#
#     mail_managers(subject=subject, message=f'Добавлен комментарий {instance.text_comment}',)

