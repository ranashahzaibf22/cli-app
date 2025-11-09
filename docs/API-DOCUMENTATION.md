# API Documentation

## Base URL

**Development:** `http://localhost:8000`  
**Production:** `https://your-api-domain.com`

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Get Token

```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=yourpassword
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

## Endpoints

### Authentication

#### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

#### Get Current User
```http
GET /api/v1/auth/me
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "body_measurements": {},
  "style_preferences": {},
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Products

#### Get Products
```http
GET /api/v1/products?skip=0&limit=20&category=shirts&min_price=20&max_price=100
```

**Query Parameters:**
- `skip` (int): Number of items to skip (pagination)
- `limit` (int): Maximum items to return (1-100)
- `category` (string): Filter by category
- `brand` (string): Filter by brand
- `min_price` (float): Minimum price
- `max_price` (float): Maximum price
- `ar_compatible` (bool): Filter AR-compatible items

**Response:**
```json
[
  {
    "id": 1,
    "name": "Classic Cotton T-Shirt",
    "description": "Comfortable everyday tee",
    "category": "shirts",
    "brand": "StyleBrand",
    "price": 29.99,
    "image_urls": ["https://example.com/image1.jpg"],
    "color_variants": ["white", "black", "navy"],
    "ar_compatible": true,
    "popularity_score": 85.5,
    "view_count": 1234,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### Get Product by ID
```http
GET /api/v1/products/1
```

#### Search Products
```http
POST /api/v1/products/search
Content-Type: application/json

{
  "query": "summer dress",
  "category": "dresses",
  "min_price": 30,
  "max_price": 150,
  "page": 1,
  "page_size": 20
}
```

#### Get Categories
```http
GET /api/v1/products/categories
```

**Response:**
```json
["shirts", "pants", "dresses", "outerwear", "shoes", "accessories"]
```

#### Get Trending Products
```http
GET /api/v1/products/trending?limit=10
```

### AR Try-On

#### Create AR Session
```http
POST /api/v1/ar/sessions
Authorization: Bearer <token>
Content-Type: application/json

{
  "clothing_item_id": 1,
  "session_type": "photo"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "clothing_item_id": 1,
  "session_type": "photo",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Upload Image for AR Processing
```http
POST /api/v1/ar/process
Authorization: Bearer <token>
Content-Type: application/json

{
  "session_id": 1,
  "image_data": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Response:**
```json
{
  "session_id": 1,
  "result_image_url": "https://example.com/result.jpg",
  "pose_landmarks": {...},
  "body_measurements": {
    "shoulder_width": 42.5,
    "torso_length": 65.3
  },
  "fit_analysis": {
    "fit_score": 85.5,
    "fit_category": "good",
    "recommendations": ["Consider size M for perfect fit"]
  },
  "quality_score": 92.3,
  "processing_time": 4.2
}
```

### Machine Learning

#### Get Size Recommendation
```http
POST /api/v1/ml/predict/size
Authorization: Bearer <token>
Content-Type: application/json

{
  "item_id": 1,
  "user_measurements": {
    "height": 175,
    "weight": 70,
    "chest": 95,
    "waist": 80,
    "hips": 98
  }
}
```

**Response:**
```json
{
  "recommended_size": "M",
  "confidence_score": 0.87,
  "alternative_sizes": [
    {"size": "S", "confidence": 0.11},
    {"size": "L", "confidence": 0.02}
  ]
}
```

#### Get Style Match Score
```http
POST /api/v1/ml/predict/style
Authorization: Bearer <token>
Content-Type: application/json

{
  "item_ids": [1, 5, 12],
  "user_preferences": {
    "style": "casual",
    "occasion": "everyday"
  }
}
```

**Response:**
```json
{
  "compatibility_score": 0.82,
  "explanation": "These items create a cohesive casual look...",
  "suggestions": ["Add neutral shoes to complete the outfit"]
}
```

#### Get Personalized Recommendations
```http
POST /api/v1/ml/recommendations
Authorization: Bearer <token>
Content-Type: application/json

{
  "recommendation_type": "personalized",
  "limit": 10,
  "context": {
    "occasion": "work",
    "season": "spring"
  }
}
```

**Response:**
```json
{
  "id": 1,
  "recommended_items": [5, 12, 18, 23, 34],
  "recommendation_type": "personalized",
  "ml_confidence_score": 0.78,
  "groq_reasoning": "Based on your browsing history...",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Analytics

#### Track User Interaction
```http
POST /api/v1/analytics/track
Authorization: Bearer <token>
Content-Type: application/json

{
  "item_id": 1,
  "interaction_type": "view",
  "session_data": {},
  "device_info": {"type": "desktop"},
  "context": {"source": "search"}
}
```

#### Get Analytics Summary
```http
GET /api/v1/analytics/summary
Authorization: Bearer <token>
```

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "detail": "Error message description"
}
```

### Common HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized (missing or invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `422` - Unprocessable Entity (validation error)
- `500` - Internal Server Error

## Rate Limiting

API requests are limited to:
- Anonymous: 100 requests/hour
- Authenticated: 1000 requests/hour

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1609459200
```

## Pagination

Endpoints returning lists support pagination:

```http
GET /api/v1/products?skip=20&limit=20
```

Response includes:
```json
{
  "items": [...],
  "total": 500,
  "skip": 20,
  "limit": 20
}
```

## Interactive Documentation

FastAPI provides interactive API documentation:

- **Swagger UI:** `http://localhost:8000/api/docs`
- **ReDoc:** `http://localhost:8000/api/redoc`
