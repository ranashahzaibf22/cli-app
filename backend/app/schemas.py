"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    body_measurements: Optional[Dict[str, Any]] = None
    style_preferences: Optional[Dict[str, Any]] = None


class UserResponse(UserBase):
    id: int
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    body_measurements: Dict[str, Any] = {}
    style_preferences: Dict[str, Any] = {}
    created_at: datetime
    
    class Config:
        from_attributes = True


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


# Clothing Item Schemas
class ClothingItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    price: float = Field(..., ge=0)


class ClothingItemCreate(ClothingItemBase):
    image_urls: List[str] = []
    color_variants: List[str] = []
    size_chart: Dict[str, Any] = {}
    materials: List[str] = []
    care_instructions: Optional[str] = None
    sustainability_score: Optional[float] = Field(None, ge=0, le=100)
    ar_compatible: bool = True
    ar_3d_model_url: Optional[str] = None


class ClothingItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_urls: Optional[List[str]] = None
    color_variants: Optional[List[str]] = None
    size_chart: Optional[Dict[str, Any]] = None


class ClothingItemResponse(ClothingItemBase):
    id: int
    image_urls: List[str] = []
    color_variants: List[str] = []
    size_chart: Dict[str, Any] = {}
    materials: List[str] = []
    care_instructions: Optional[str] = None
    sustainability_score: Optional[float] = None
    ar_compatible: bool = True
    ar_3d_model_url: Optional[str] = None
    popularity_score: float = 0.0
    view_count: int = 0
    try_on_count: int = 0
    ml_features: Dict[str, Any] = {}
    created_at: datetime
    
    class Config:
        from_attributes = True


# AR Session Schemas
class ARSessionCreate(BaseModel):
    clothing_item_id: int
    session_type: str = Field(..., pattern="^(photo|live)$")


class ARSessionResponse(BaseModel):
    id: int
    user_id: int
    clothing_item_id: int
    session_type: str
    input_image_url: Optional[str] = None
    result_image_url: Optional[str] = None
    pose_landmarks: Dict[str, Any] = {}
    body_measurements_detected: Dict[str, Any] = {}
    fit_analysis: Dict[str, Any] = {}
    quality_score: Optional[float] = None
    processing_time: Optional[float] = None
    user_rating: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class ARProcessRequest(BaseModel):
    session_id: int
    image_data: str  # base64 encoded image


class FitAnalysisResponse(BaseModel):
    fit_score: float = Field(..., ge=0, le=100)
    fit_category: str  # loose/perfect/tight
    recommendations: List[str] = []
    measurements: Dict[str, Any] = {}


# ML Model Schemas
class MLModelResponse(BaseModel):
    id: int
    model_name: str
    model_type: str
    version: str
    status: str
    accuracy_metrics: Dict[str, Any] = {}
    performance_metrics: Dict[str, Any] = {}
    training_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class SizeRecommendationRequest(BaseModel):
    item_id: int
    user_measurements: Dict[str, float]


class SizeRecommendationResponse(BaseModel):
    recommended_size: str
    confidence_score: float = Field(..., ge=0, le=1)
    alternative_sizes: List[Dict[str, Any]] = []


class StyleMatchRequest(BaseModel):
    item_ids: List[int]
    user_preferences: Optional[Dict[str, Any]] = None


class StyleMatchResponse(BaseModel):
    compatibility_score: float = Field(..., ge=0, le=1)
    explanation: str
    suggestions: List[str] = []


# Recommendation Schemas
class RecommendationRequest(BaseModel):
    recommendation_type: str = "personalized"
    context: Optional[Dict[str, Any]] = None
    limit: int = Field(10, ge=1, le=50)


class RecommendationResponse(BaseModel):
    id: int
    recommended_items: List[int]
    recommendation_type: str
    ml_confidence_score: Optional[float] = None
    groq_reasoning: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Analytics Schemas
class InteractionCreate(BaseModel):
    item_id: int
    interaction_type: str = Field(..., pattern="^(view|like|try-on|purchase)$")
    session_data: Optional[Dict[str, Any]] = None
    device_info: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None


class AnalyticsResponse(BaseModel):
    total_interactions: int
    interaction_breakdown: Dict[str, int]
    popular_items: List[Dict[str, Any]]
    user_engagement: Dict[str, Any]
    ar_usage: Dict[str, Any]


# Search and Filter Schemas
class ProductSearchRequest(BaseModel):
    query: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    colors: Optional[List[str]] = None
    sizes: Optional[List[str]] = None
    ar_compatible: Optional[bool] = None
    sort_by: Optional[str] = "popularity"
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
