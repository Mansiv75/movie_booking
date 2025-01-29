# Movie Booking System API

## Overview
This project is a Django-based API for managing a movie booking system. The system allows users to fetch movie and theater details, add new movies, book tickets, and ensure seat availability.

## Features
- Fetch movie details by ID (GET API)
- Add a new movie record (POST API)
- Check seat availability and prevent overlapping showtimes
- Fetch theater details by ID (GET API)
- Create new movie bookings (POST API)

## Tech Stack
- **Backend:** Django, Django REST Framework (DRF)
- **Database:** SQLite (default, can be changed to PostgreSQL/MySQL)
- **Tools:** Python, Django ORM

## Installation
### Prerequisites
- Python 3.9+
- Virtual environment (optional but recommended)
- Django installed (`pip install django djangorestframework`)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/movie-booking-api.git
   cd movie-booking-api
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```sh
   python manage.py migrate
   ```
5. Run the server:
   ```sh
   python manage.py runserver
   ```

## API Endpoints
### 1. Fetch Movie Details by ID
**Endpoint:** `GET /movies/<int:movie_id>/`

**Response:**
```json
{
  "id": 1,
  "title": "Inception",
  "genre": "Sci-Fi",
  "duration": 148,
  "language": "English"
}
```

### 2. Add a New Movie
**Endpoint:** `POST /movies/`

**Request Body:**
```json
{
  "title": "Parasite",
  "genre": "Thriller",
  "duration": 132,
  "language": "Korean"
}
```

**Response:**
```json
{
  "id": 2,
  "title": "Parasite",
  "genre": "Thriller",
  "duration": 132,
  "language": "Korean"
}
```

### 3. Check Seat Availability and Prevent Overlapping Bookings
(Implementation logic will handle seat availability before booking a movie.)

### 4. Fetch Theater Details by ID
**Endpoint:** `GET /theaters/<int:theater_id>/`

**Response:**
```json
{
  "id": 1,
  "name": "IMAX Cinema",
  "location": "Downtown",
  "capacity": 200
}
```

### 5. Create a Movie Booking
**Endpoint:** `POST /bookings/`

**Request Body:**
```json
{
  "user_id": 3,
  "movie_id": 1,
  "theater_id": 2,
  "showtime": "2025-02-01T18:00:00Z",
  "seats": 2
}
```

**Response:**
```json
{
  "id": 5,
  "user_id": 3,
  "movie_id": 1,
  "theater_id": 2,
  "showtime": "2025-02-01T18:00:00Z",
  "seats": 2
}
```


## Future Improvements
- Add authentication for user-based booking management
- Integrate payment gateways
- Implement caching with Redis for improved performance
