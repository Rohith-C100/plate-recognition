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
    path('fine/<str:pnum>', views.fine_vehicle,name='fine'),
    path('complain/<str:pnum>', views.complain_vehicle,name='complain'),
    path('success', views.success,name='success'),
    path('notexist', views.notexist,name='notexist'),
    path('vehical/<str:pk>', views.VehicalDetailView.as_view(),name='vehical'),
    path('search', views.search,name='search'),
    path('history', views.vehical_histroy,name='history'),
    path('complain_details/<int:pk>', views.ComplainDetailView.as_view(),name='complain_detail'),
    path('fine_details/<int:pk>', views.FineDetailView.as_view(),name='fine_detail'),
]
