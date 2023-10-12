from . import views
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('',views.all_specimen,name='specimen'),
    path('register/',views.register_account,name='register'),
    path('update_user/',views.update_account,name='update_user'),
    path('login/',views.login_account,name='login'),
    path('logout/',views.logout_account,name='logout'),
    path('create/',views.create_specimen, name='create'),
    path('update/',views.update_specimen,name='update'),
    path('delete/',views.delete_specimen,name='delete')
]
