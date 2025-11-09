"""SQLAlchemy database models"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """User model with profile and measurements"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    bio = Column(Text)
    profile_picture = Column(String(500))
    
    # Body measurements (JSON: height, weight, chest, waist, hips, etc.)
    body_measurements = Column(JSON, default={})
    
    # Style preferences (JSON: colors, styles, occasions, brands)
    style_preferences = Column(JSON, default={})
    
    # Interaction history (JSON: views, likes, purchases, try-ons)
    interaction_history = Column(JSON, default={})
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    ar_sessions = relationship("ARSession", back_populates="user")
    interactions = relationship("UserInteraction", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")


class ClothingItem(Base):
    """Clothing item model with detailed attributes"""
    __tablename__ = "clothing_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(100), index=True)
    subcategory = Column(String(100))
    brand = Column(String(100), index=True)
    price = Column(Float)
    
    # Image and variants (JSON arrays)
    image_urls = Column(JSON, default=[])
    color_variants = Column(JSON, default=[])
    size_chart = Column(JSON, default={})
    
    # Materials and care
    materials = Column(JSON, default=[])
    care_instructions = Column(Text)
    sustainability_score = Column(Float)
    
    # AR capabilities
    ar_compatible = Column(Boolean, default=True)
    ar_3d_model_url = Column(String(500))
    
    # Analytics
    popularity_score = Column(Float, default=0.0)
    view_count = Column(Integer, default=0)
    try_on_count = Column(Integer, default=0)
    
    # ML features (JSON: extracted features for ML models)
    ml_features = Column(JSON, default={})
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    ar_sessions = relationship("ARSession", back_populates="clothing_item")
    interactions = relationship("UserInteraction", back_populates="item")


class ARSession(Base):
    """AR try-on session with pose detection and fit analysis"""
    __tablename__ = "ar_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    clothing_item_id = Column(Integer, ForeignKey("clothing_items.id"), nullable=False)
    
    session_type = Column(String(50))  # photo/live
    input_image_url = Column(String(500))
    result_image_url = Column(String(500))
    
    # Pose and body data (JSON)
    pose_landmarks = Column(JSON, default={})
    body_measurements_detected = Column(JSON, default={})
    fit_analysis = Column(JSON, default={})
    
    # Quality metrics
    quality_score = Column(Float)
    processing_time = Column(Float)  # seconds
    user_rating = Column(Integer)  # 1-5
    
    # Metadata (JSON: camera settings, lighting, etc.)
    ar_metadata = Column(JSON, default={})
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="ar_sessions")
    clothing_item = relationship("ClothingItem", back_populates="ar_sessions")


class MLModel(Base):
    """ML model tracking and versioning"""
    __tablename__ = "ml_models"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(255), nullable=False, index=True)
    model_type = Column(String(100))  # classifier/recommender/matcher
    version = Column(String(50))
    file_path = Column(String(500))
    
    # Training metrics
    training_data_size = Column(Integer)
    accuracy_metrics = Column(JSON, default={})
    performance_metrics = Column(JSON, default={})
    
    training_date = Column(DateTime(timezone=True))
    status = Column(String(50), default="training")  # training/ready/deprecated
    description = Column(Text)


class UserInteraction(Base):
    """User interaction tracking for analytics"""
    __tablename__ = "user_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("clothing_items.id"), nullable=False)
    
    interaction_type = Column(String(50), index=True)  # view/like/try-on/purchase
    session_data = Column(JSON, default={})
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    device_info = Column(JSON, default={})
    
    # Context (JSON: search query, referrer, etc.)
    context = Column(JSON, default={})
    
    # Relationships
    user = relationship("User", back_populates="interactions")
    item = relationship("ClothingItem", back_populates="interactions")


class Recommendation(Base):
    """Personalized recommendations with ML confidence"""
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    recommended_items = Column(JSON, default=[])  # list of item IDs
    recommendation_type = Column(String(100))  # personalized/trending/similar
    
    # Context and reasoning
    context = Column(JSON, default={})  # occasion, weather, preferences
    ml_confidence_score = Column(Float)
    groq_reasoning = Column(Text)
    
    # Performance metrics
    user_feedback = Column(Integer)  # -1, 0, 1
    click_through_rate = Column(Float)
    conversion_rate = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="recommendations")
