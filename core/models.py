from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Movie(models.Model):
    title= models.CharField(max_length=200)
    genre=models.CharField(max_length=200)
    duration= models.PositiveIntegerField()
    language= models.CharField(max_length=50)
    

    def __str__(self):
        return self.title

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="showtimes")
    start_time = models.DateTimeField()  
    end_time = models.DateTimeField()    
    total_seats = models.PositiveIntegerField() 
    available_seats = models.PositiveIntegerField()  

    def __str__(self):
        return f"{self.movie.title} - {self.start_time}"

    def check_seat_availability(self, seats_requested):
        return self.available_seats >= seats_requested

    def book_seats(self, seats_requested):
        if self.check_seat_availability(seats_requested):
            self.available_seats -= seats_requested
            self.save()
            return True
        return False

    @staticmethod
    def check_for_overlap(start_time, end_time, movie_id):
        overlapping_showtimes = Showtime.objects.filter(
            movie_id=movie_id,
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        return overlapping_showtimes.exists()

class Theater(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    seating_capacity = models.IntegerField()  # Total seating capacity

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    seats_booked = models.IntegerField()

    def __str__(self):
        return f"Booking for {self.movie.title} by {self.user.username} on {self.showtime.start_time}"

    def is_seat_available(self):
        return self.showtime.check_seat_availability(self.seats_booked)

    def book_seats(self):
        if self.is_seat_available():
            self.showtime.book_seats(self.seats_booked)
            self.save()
            return True
        return False