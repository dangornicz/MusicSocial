from django.urls import path
from . import views

urlpatterns = [
    path('', views.load_user_data, name='load'),
    path('save_event/', views.save_event, name='save_event'),
    path('delete_event/<int:event_id>', views.delete_event, name='delete_event'),
    path('user_search/', views.user_search, name='user_search'),
    path('save_comment/', views.save_comment, name='save_comment'),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('update_comment/<int:comment_id>', views.update_comment, name='update_comment'),
    path('profile/', views.profile, name='profile')

]
