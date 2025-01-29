from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
import json

def get_movie_by_id(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
        data={
            'id': movie.id,
            'title': movie.title,
            'genre': movie.genre,
            'duration': movie.duration,
            'language': movie.language,
            
        }
        return JsonResponse(data, status=200)

    except Movie.DoesNotExist:
        return JsonResponse( {"error":"movie not found"}, status=404)

@csrf_exempt
def create_movie(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            genre = data.get('genre')
            duration = data.get('duration')
            language = data.get('language')

            movie=Movie.objects.create(
                title=title,
                genre=genre,
                duration=duration,
                language=language,
            )
            return JsonResponse({"message":"movie created successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
         return JsonResponse({"error": "Invalid method. Only POST allowed."}, status=405)
    

@csrf_exempt
def add_showtime(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            movie_id = data.get('movie_id')
            start_time = parse_datetime(data.get('start_time'))
            end_time = parse_datetime(data.get('end_time'))
            total_seats = data.get('total_seats')

            if not movie_id or not start_time or not end_time or not total_seats:
                return JsonResponse({"error": "Missing required fields."}, status=400)

            
            if Showtime.check_for_overlap(start_time, end_time, movie_id):
                return JsonResponse({"error": "Overlapping showtimes detected."}, status=400)

            
            movie = Movie.objects.get(id=movie_id)
            showtime = Showtime.objects.create(
                movie=movie,
                start_time=start_time,
                end_time=end_time,
                total_seats=total_seats,
                available_seats=total_seats,  # Initially, available seats = total seats
            )

            return JsonResponse({
                "message": "Showtime added successfully",
                "showtime_id": showtime.id
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid method. Only POST allowed."}, status=405)

def get_theater(request, theater_id):
    if request.method == "GET":
        # Fetch the theater by its ID
        theater = get_object_or_404(Theater, id=theater_id)
        
        # Return the theater details as JSON
        return JsonResponse({
            "id": theater.id,
            "name": theater.name,
            "location": theater.location,
            "seating_capacity": theater.seating_capacity
        })

@csrf_exempt
def create_booking(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            user_id = data.get('user_id')
            movie_id = data.get('movie_id')
            showtime_id = data.get('showtime_id')
            seats_booked = data.get('seats_booked')

            # Check if required fields are provided
            if not user_id or not movie_id or not showtime_id or not seats_booked:
                return JsonResponse({"error": "Missing required fields."}, status=400)

            # Fetch user, movie, and showtime from the database
            user = User.objects.get(id=user_id)
            movie = Movie.objects.get(id=movie_id)
            showtime = Showtime.objects.get(id=showtime_id)

            # Create a booking instance
            booking = Booking(
                user=user,
                movie=movie,
                showtime=showtime,
                seats_booked=seats_booked
            )

            # Try to book the seats
            if booking.book_seats():
                return JsonResponse({
                    "message": "Booking successful!",
                    "booking_id": booking.id
                }, status=201)

            return JsonResponse({"error": "Not enough seats available."}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
        except Movie.DoesNotExist:
            return JsonResponse({"error": "Movie not found."}, status=404)
        except Showtime.DoesNotExist:
            return JsonResponse({"error": "Showtime not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid method. Only POST allowed."}, status=40)