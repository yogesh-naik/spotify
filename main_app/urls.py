from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"), # <- here we have added the new path
    path('about/', views.About.as_view(), name="about"),
    
    path('artists/', views.ArtistList.as_view(), name="artist_list"),
    
    #Funcation based views
    path('artists/<int:pk>/', views.SingleArtistDetail, name="artist_detail"),
    path('artists/new/', views.createArtist, name="artist_create"),
    path('artists/<int:pk>/update',views.ArtistUpdate, name="artist_update"),
    path('artists/<int:pk>/delete',views.deleteArtist, name="artist_delete"),
    
    #CBV
       # path('artists/new/', views.ArtistCreate.as_view(), name="artist_create"),
    #    path('artists/<int:pk>/', views.ArtistDetail.as_view(), name="artist_detail"),
    # path('artists/<int:pk>/update',views.ArtistUpdate.as_view(), name="artist_update"),
    
    path('stocks/', views.Stocks.as_view(), name="stock_list"),
]