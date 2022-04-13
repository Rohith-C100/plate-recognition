from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [
    path('signup', views.signup, name='signup'),
    path('image_upload',views.image_upload_view, name = 'image_upload'),
    path('success', views.success, name = 'success'),
    path('identify/<int:pk>', views.identify, name = 'identify'),
    path('display/<int:pk>', views.display,name='display'),
]
