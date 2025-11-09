"""Database CRUD operations"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc
from datetime import datetime

from app import models, schemas
from app.auth import get_password_hash


# User CRUD
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user"""
    db_user = models.User(
        email=user.email,
        username=user.username,
        password_hash=get_password_hash(user.password),
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get user by email"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Get user by username"""
    return db.query(models.User).filter(models.User.username == username).first()


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> models.User:
    """Update user profile"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


# Clothing Item CRUD
def create_clothing_item(db: Session, item: schemas.ClothingItemCreate) -> models.ClothingItem:
    """Create a new clothing item"""
    db_item = models.ClothingItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_clothing_item(db: Session, item_id: int) -> Optional[models.ClothingItem]:
    """Get clothing item by ID"""
    return db.query(models.ClothingItem).filter(models.ClothingItem.id == item_id).first()


def get_clothing_items(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    ar_compatible: Optional[bool] = None
) -> List[models.ClothingItem]:
    """Get clothing items with filters"""
    query = db.query(models.ClothingItem)
    
    if category:
        query = query.filter(models.ClothingItem.category == category)
    
    if brand:
        query = query.filter(models.ClothingItem.brand == brand)
    
    if min_price is not None:
        query = query.filter(models.ClothingItem.price >= min_price)
    
    if max_price is not None:
        query = query.filter(models.ClothingItem.price <= max_price)
    
    if ar_compatible is not None:
        query = query.filter(models.ClothingItem.ar_compatible == ar_compatible)
    
    return query.order_by(desc(models.ClothingItem.popularity_score)).offset(skip).limit(limit).all()


def search_clothing_items(
    db: Session,
    query: str,
    skip: int = 0,
    limit: int = 20
) -> List[models.ClothingItem]:
    """Search clothing items by name or description"""
    search_filter = or_(
        models.ClothingItem.name.ilike(f"%{query}%"),
        models.ClothingItem.description.ilike(f"%{query}%"),
        models.ClothingItem.brand.ilike(f"%{query}%")
    )
    
    return db.query(models.ClothingItem).filter(search_filter).offset(skip).limit(limit).all()


def update_clothing_item(
    db: Session,
    item_id: int,
    item_update: schemas.ClothingItemUpdate
) -> Optional[models.ClothingItem]:
    """Update clothing item"""
    db_item = db.query(models.ClothingItem).filter(models.ClothingItem.id == item_id).first()
    
    if not db_item:
        return None
    
    update_data = item_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item


def increment_view_count(db: Session, item_id: int):
    """Increment view count for item"""
    db_item = db.query(models.ClothingItem).filter(models.ClothingItem.id == item_id).first()
    if db_item:
        db_item.view_count += 1
        db.commit()


def increment_tryon_count(db: Session, item_id: int):
    """Increment try-on count for item"""
    db_item = db.query(models.ClothingItem).filter(models.ClothingItem.id == item_id).first()
    if db_item:
        db_item.try_on_count += 1
        db.commit()


# AR Session CRUD
def create_ar_session(
    db: Session,
    user_id: int,
    session_create: schemas.ARSessionCreate
) -> models.ARSession:
    """Create a new AR session"""
    db_session = models.ARSession(
        user_id=user_id,
        clothing_item_id=session_create.clothing_item_id,
        session_type=session_create.session_type
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def get_ar_session(db: Session, session_id: int) -> Optional[models.ARSession]:
    """Get AR session by ID"""
    return db.query(models.ARSession).filter(models.ARSession.id == session_id).first()


def get_user_ar_sessions(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 20
) -> List[models.ARSession]:
    """Get user's AR sessions"""
    return db.query(models.ARSession).filter(
        models.ARSession.user_id == user_id
    ).order_by(desc(models.ARSession.created_at)).offset(skip).limit(limit).all()


def update_ar_session(db: Session, session_id: int, **kwargs) -> Optional[models.ARSession]:
    """Update AR session with processing results"""
    db_session = db.query(models.ARSession).filter(models.ARSession.id == session_id).first()
    
    if not db_session:
        return None
    
    for field, value in kwargs.items():
        if hasattr(db_session, field):
            setattr(db_session, field, value)
    
    db.commit()
    db.refresh(db_session)
    return db_session


# User Interaction CRUD
def create_interaction(
    db: Session,
    user_id: int,
    interaction: schemas.InteractionCreate
) -> models.UserInteraction:
    """Create user interaction record"""
    db_interaction = models.UserInteraction(
        user_id=user_id,
        item_id=interaction.item_id,
        interaction_type=interaction.interaction_type,
        session_data=interaction.session_data or {},
        device_info=interaction.device_info or {},
        context=interaction.context or {}
    )
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction


def get_user_interactions(
    db: Session,
    user_id: int,
    interaction_type: Optional[str] = None,
    limit: int = 100
) -> List[models.UserInteraction]:
    """Get user interactions"""
    query = db.query(models.UserInteraction).filter(models.UserInteraction.user_id == user_id)
    
    if interaction_type:
        query = query.filter(models.UserInteraction.interaction_type == interaction_type)
    
    return query.order_by(desc(models.UserInteraction.timestamp)).limit(limit).all()


# Recommendation CRUD
def create_recommendation(
    db: Session,
    user_id: int,
    recommended_items: List[int],
    recommendation_type: str,
    context: Dict[str, Any] = None,
    ml_confidence_score: Optional[float] = None,
    groq_reasoning: Optional[str] = None
) -> models.Recommendation:
    """Create recommendation record"""
    db_recommendation = models.Recommendation(
        user_id=user_id,
        recommended_items=recommended_items,
        recommendation_type=recommendation_type,
        context=context or {},
        ml_confidence_score=ml_confidence_score,
        groq_reasoning=groq_reasoning
    )
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    return db_recommendation


def get_user_recommendations(
    db: Session,
    user_id: int,
    limit: int = 10
) -> List[models.Recommendation]:
    """Get user recommendations"""
    return db.query(models.Recommendation).filter(
        models.Recommendation.user_id == user_id
    ).order_by(desc(models.Recommendation.created_at)).limit(limit).all()


# ML Model CRUD
def create_ml_model(db: Session, model_data: Dict[str, Any]) -> models.MLModel:
    """Create ML model record"""
    db_model = models.MLModel(**model_data)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def get_ml_models(db: Session, model_type: Optional[str] = None) -> List[models.MLModel]:
    """Get ML models"""
    query = db.query(models.MLModel)
    
    if model_type:
        query = query.filter(models.MLModel.model_type == model_type)
    
    return query.filter(models.MLModel.status == "ready").all()


def get_latest_model(db: Session, model_name: str) -> Optional[models.MLModel]:
    """Get latest version of a model"""
    return db.query(models.MLModel).filter(
        models.MLModel.model_name == model_name,
        models.MLModel.status == "ready"
    ).order_by(desc(models.MLModel.training_date)).first()
