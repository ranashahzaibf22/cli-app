"""AR try-on routes"""
import base64
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import numpy as np
import cv2

from app import crud, schemas, auth, models
from app.database import get_db
from app.utils.pose_detection import PoseDetector, analyze_fit_from_pose
from app.utils.image_processing import decode_base64_image, encode_image_to_base64

router = APIRouter()


@router.post("/sessions", response_model=schemas.ARSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_ar_session(
    session_create: schemas.ARSessionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Create a new AR try-on session"""
    # Verify item exists
    item = crud.get_clothing_item(db, session_create.clothing_item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clothing item not found"
        )
    
    # Increment try-on count
    crud.increment_tryon_count(db, session_create.clothing_item_id)
    
    # Create session
    session = crud.create_ar_session(db, current_user.id, session_create)
    
    return session


@router.get("/sessions", response_model=List[schemas.ARSessionResponse])
async def get_user_ar_sessions(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get user's AR sessions"""
    sessions = crud.get_user_ar_sessions(db, current_user.id, skip, limit)
    return sessions


@router.get("/sessions/{session_id}", response_model=schemas.ARSessionResponse)
async def get_ar_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Get specific AR session"""
    session = crud.get_ar_session(db, session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this session"
        )
    
    return session


@router.post("/process", response_model=schemas.ARSessionResponse)
async def process_ar_image(
    ar_request: schemas.ARProcessRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Process AR try-on with pose detection"""
    import time
    start_time = time.time()
    
    # Get session
    session = crud.get_ar_session(db, ar_request.session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    try:
        # Decode image
        image = decode_base64_image(ar_request.image_data)
        
        # Initialize pose detector
        detector = PoseDetector()
        
        # Detect pose
        pose_result = detector.detect_pose(image)
        
        if not pose_result or not pose_result.get('landmarks'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not detect pose in image. Please ensure you're facing the camera with good lighting."
            )
        
        landmarks = pose_result['landmarks']
        
        # Calculate quality score
        quality_score = detector.get_pose_quality_score(landmarks)
        
        if quality_score < 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pose quality too low. Please stand facing the camera with your full body visible."
            )
        
        # Extract body measurements
        measurements = detector.extract_body_measurements(landmarks, image.shape)
        
        # Get item for fit analysis
        item = crud.get_clothing_item(db, session.clothing_item_id)
        
        # Perform fit analysis (simplified for now)
        fit_analysis = {
            'fit_score': 85.0,
            'fit_category': 'good',
            'recommendations': ['Size M recommended based on measurements']
        }
        
        # Draw pose on image (for visualization)
        result_image = detector.draw_pose(image, landmarks)
        
        # Encode result image
        result_image_data = encode_image_to_base64(result_image)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Update session with results
        updated_session = crud.update_ar_session(
            db,
            ar_request.session_id,
            result_image_url=result_image_data[:100],  # Store preview
            pose_landmarks={"landmarks": landmarks[:10]},  # Store subset
            body_measurements_detected=measurements,
            fit_analysis=fit_analysis,
            quality_score=quality_score,
            processing_time=processing_time
        )
        
        # Clean up
        detector.close()
        
        return updated_session
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing image: {str(e)}"
        )


@router.post("/analyze-fit", response_model=schemas.FitAnalysisResponse)
async def analyze_fit(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Analyze fit for a processed AR session"""
    session = crud.get_ar_session(db, session_id)
    
    if not session or session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    if not session.body_measurements_detected:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session not yet processed. Please upload an image first."
        )
    
    # Get item
    item = crud.get_clothing_item(db, session.clothing_item_id)
    
    # Analyze fit
    fit_result = session.fit_analysis or {
        'fit_score': 85.0,
        'fit_category': 'good',
        'recommendations': ['Consider size M for best fit'],
        'measurements': session.body_measurements_detected
    }
    
    return schemas.FitAnalysisResponse(**fit_result)


@router.post("/rate", status_code=status.HTTP_200_OK)
async def rate_ar_result(
    session_id: int,
    rating: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Rate AR try-on result"""
    if rating < 1 or rating > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5"
        )
    
    session = crud.get_ar_session(db, session_id)
    
    if not session or session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Update rating
    crud.update_ar_session(db, session_id, user_rating=rating)
    
    return {"message": "Rating saved successfully"}
