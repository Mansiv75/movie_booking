from django.urls import path
from . import views

urlpatterns = [
    path('movies/<int:movie_id>/', views.get_movie_by_id, name='get_movie_by_id'),
    path('movies/', views.create_movie, name='add_movie'),
    path('movies/showtime/', views.add_showtime, name='add_showtime'),
    path('theater/<int:theater_id>/', views.get_theater, name='get_theater'),
    path('movies/booking/', views.create_booking, name='create_booking'),
]
