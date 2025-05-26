from django.urls import path
from .import views

app_name = 'core'

urlpatterns = [
    
    path('',views.index, name='index'),
    path('upload_ruc/',views.upload_ruc, name='upload_ruc'),
    path('visualize_ruc/',views.visualize_ruc, name='visualize_ruc'),
    path('sort_ruc_timsort/', views.sort_ruc_timsort, name= 'sort_ruc_timsort'),
    path('sort_quicksort/', views.sort_quicksort, name= 'sort_quicksort')

]
