from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_feed, name='newsfeed'),
    path('save_event/', views.save_event, name='save_event'),
    path('delete_event/<int:event_id>', views.delete_event, name='delete_event'),
    path('user_search/', views.user_search, name='user_search'),
    path('save_comment/', views.save_comment, name='save_comment'),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('update_comment/<int:comment_id>', views.update_comment, name='update_comment'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('profile_search/', views.profile_search, name='profile_search'),
    path('follow/<str:username>', views.follow, name='follow'),
    path('unfollow/<str:username>', views.unfollow, name='unfollow'),
    path('bio/', views.bio, name="bio"),
    path('save_comment_profile/<str:username>', views.save_comment_profile, name='save_comment_profile'),
    path('delete_comment_profile/<int:comment_id>/<str:username>', views.delete_comment_profile,
         name='delete_comment_profile'),
    path('update_comment_profile/<int:comment_id>/<str:username>', views.update_comment_profile,
         name='update_comment_profile'),

]
