"""ML model routes"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas, auth, models
from app.database import get_db

router = APIRouter()


@router.get("/models/status", response_model=List[schemas.MLModelResponse])
async def get_ml_models_status(
    model_type: str = None,
    db: Session = Depends(get_db)
):
    """Get status of ML models"""
    models_list = crud.get_ml_models(db, model_type)
    return models_list


@router.post("/predict/size", response_model=schemas.SizeRecommendationResponse)
async def predict_size(
    request: schemas.SizeRecommendationRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Predict recommended size for user and item"""
    # Get item
    item = crud.get_clothing_item(db, request.item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    # Simplified size recommendation logic
    # In production, this would use the actual ML model
    measurements = request.user_measurements
    
    # Simple heuristic based on chest/waist measurements
    if 'chest' in measurements:
        chest = measurements['chest']
        if chest < 90:
            size = 'S'
            confidence = 0.85
        elif chest < 100:
            size = 'M'
            confidence = 0.88
        elif chest < 110:
            size = 'L'
            confidence = 0.86
        else:
            size = 'XL'
            confidence = 0.84
    else:
        size = 'M'
        confidence = 0.70
    
    alternatives = [
        {'size': 'S', 'confidence': 0.15},
        {'size': 'L', 'confidence': 0.10}
    ] if size == 'M' else []
    
    return schemas.SizeRecommendationResponse(
        recommended_size=size,
        confidence_score=confidence,
        alternative_sizes=alternatives
    )


@router.post("/predict/style", response_model=schemas.StyleMatchResponse)
async def predict_style_match(
    request: schemas.StyleMatchRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Predict style compatibility for outfit"""
    # Get items
    items = []
    for item_id in request.item_ids:
        item = crud.get_clothing_item(db, item_id)
        if item:
            items.append(item)
    
    if len(items) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Need at least 2 items for style matching"
        )
    
    # Simplified style matching logic
    # Check if items are from same style category
    categories = [item.category for item in items]
    unique_categories = len(set(categories))
    
    # More diverse categories = better outfit
    if unique_categories >= len(items):
        score = 0.85
        explanation = "Great combination! These items complement each other well."
        suggestions = []
    elif unique_categories >= len(items) * 0.7:
        score = 0.70
        explanation = "Good mix of items. Consider adding accessories."
        suggestions = ["Add a complementary accessory"]
    else:
        score = 0.55
        explanation = "This combination might work but needs refinement."
        suggestions = ["Try mixing different item types", "Consider color harmony"]
    
    return schemas.StyleMatchResponse(
        compatibility_score=score,
        explanation=explanation,
        suggestions=suggestions
    )


@router.post("/recommendations", response_model=schemas.RecommendationResponse)
async def get_recommendations(
    request: schemas.RecommendationRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get personalized recommendations"""
    # Get user's interaction history
    interactions = crud.get_user_interactions(db, current_user.id, limit=50)
    
    # Get items user has interacted with
    interacted_item_ids = [i.item_id for i in interactions]
    
    # Get trending items excluding already viewed
    all_items = crud.get_clothing_items(db, limit=100)
    recommended_items = [
        item.id for item in all_items
        if item.id not in interacted_item_ids
    ][:request.limit]
    
    # Create recommendation record
    recommendation = crud.create_recommendation(
        db,
        user_id=current_user.id,
        recommended_items=recommended_items,
        recommendation_type=request.recommendation_type,
        context=request.context or {},
        ml_confidence_score=0.75,
        groq_reasoning="Based on your browsing history and current trends."
    )
    
    return recommendation


@router.get("/model/performance")
async def get_model_performance(
    model_name: str,
    db: Session = Depends(get_db)
):
    """Get ML model performance metrics"""
    model = crud.get_latest_model(db, model_name)
    
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found"
        )
    
    return {
        'model_name': model.model_name,
        'version': model.version,
        'status': model.status,
        'accuracy_metrics': model.accuracy_metrics,
        'performance_metrics': model.performance_metrics,
        'training_date': model.training_date
    }
