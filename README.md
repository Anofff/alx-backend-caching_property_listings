# Django + Redis Property Listing Project

A Django project that demonstrates caching strategies using Redis for property listings.

## Features

- **Property Listings**: Manage property listings with title, description, price, and location
- **View-Level Caching**: Cache the property list view for 15 minutes using `@cache_page` decorator
- **Low-Level Caching**: Cache property queryset for 1 hour using Django's cache API
- **Cache Invalidation**: Automatically invalidate cache when properties are created, updated, or deleted using signals
- **Cache Metrics**: Monitor Redis cache hit/miss statistics

## Setup

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- pip

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start PostgreSQL and Redis using Docker Compose:
```bash
docker-compose up -d
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## Usage

### Accessing Property Listings

- View all properties: http://localhost:8000/properties/
- View cache metrics: http://localhost:8000/properties/metrics/

### Admin Panel

- Access admin panel: http://localhost:8000/admin/
- Login with your superuser credentials
- Manage properties through the admin interface

### Testing Caching

1. Visit http://localhost:8000/properties/ - First visit will load from database
2. Refresh the page - Subsequent visits will load from cache (15-minute view cache)
3. Create/update/delete a property in admin - Cache will be automatically invalidated
4. Check cache metrics at http://localhost:8000/properties/metrics/

## Project Structure

```
alx-backend-caching_property_listings/
├── alx_backend_caching_property_listings/
│   ├── settings.py          # Django settings with Redis cache configuration
│   └── urls.py              # Main URL configuration
├── properties/
│   ├── models.py            # Property model
│   ├── views.py             # Property list view with caching
│   ├── utils.py             # Low-level caching functions and metrics
│   ├── signals.py           # Cache invalidation signals
│   ├── apps.py              # App configuration with signal registration
│   └── urls.py              # Property URLs
├── docker-compose.yml       # PostgreSQL and Redis services
└── requirements.txt         # Python dependencies
```

## Caching Strategies

### 1. View-Level Caching
- Uses `@cache_page(60 * 15)` decorator
- Caches the entire HTTP response for 15 minutes
- Cache key is based on the request URL

### 2. Low-Level Caching
- Uses Django's `cache.get()` and `cache.set()` API
- Caches the property queryset for 1 hour (3600 seconds)
- Cache key: `all_properties`

### 3. Cache Invalidation
- Uses Django signals (`post_save`, `post_delete`)
- Automatically clears cache when properties are modified
- Ensures users always see up-to-date data

## Cache Metrics

The project includes Redis cache metrics monitoring:
- Keyspace hits
- Keyspace misses
- Hit ratio percentage
- Total requests

Access metrics at `/properties/metrics/` endpoint or check application logs.

## Docker Services

- **PostgreSQL**: Running on port 5432
- **Redis**: Running on port 6379

## Configuration

### Database
- Database: `property_listings_db`
- User: `postgres`
- Password: `postgres`
- Host: `localhost`
- Port: `5432`

### Redis Cache
- Location: `redis://127.0.0.1:6379/1`
- Key prefix: `property_listings`
- Default timeout: 3600 seconds (1 hour)

## Testing

1. Start Docker services: `docker-compose up -d`
2. Run migrations: `python manage.py migrate`
3. Create test properties via admin panel
4. Visit `/properties/` and verify caching
5. Check cache metrics at `/properties/metrics/`
6. Create/update/delete properties and verify cache invalidation
