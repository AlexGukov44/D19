from django.urls import path

from .views import *

urlpatterns = [
    path('', PostsViews.as_view(), name='posts_list'),
    path('<int:pk>', create_comment, name = 'post_detail' ),
    path('create/', PostsCreate.as_view()),
    path('<int:pk>/update/', PostsUpdate.as_view()),
    path('<int:pk>/delete/', PostsDelete.as_view()),
    # path('<int:pk>/comments/', CommentsDelete.as_view(), name='post_comments'),
]