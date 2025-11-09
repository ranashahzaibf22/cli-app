"""Product management routes"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app import crud, schemas, auth, models
from app.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.ClothingItemResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: schemas.ClothingItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Create a new clothing item"""
    return crud.create_clothing_item(db=db, item=product)


@router.get("/", response_model=List[schemas.ClothingItemResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    ar_compatible: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get clothing items with filters"""
    items = crud.get_clothing_items(
        db=db,
        skip=skip,
        limit=limit,
        category=category,
        brand=brand,
        min_price=min_price,
        max_price=max_price,
        ar_compatible=ar_compatible
    )
    return items


@router.get("/categories", response_model=List[str])
async def get_categories(db: Session = Depends(get_db)):
    """Get all unique product categories"""
    categories = db.query(models.ClothingItem.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]]


@router.get("/trending", response_model=List[schemas.ClothingItemResponse])
async def get_trending_products(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get trending products"""
    items = db.query(models.ClothingItem).order_by(
        models.ClothingItem.popularity_score.desc()
    ).limit(limit).all()
    return items


@router.get("/{item_id}", response_model=schemas.ClothingItemResponse)
async def get_product(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Get clothing item by ID"""
    item = crud.get_clothing_item(db=db, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Increment view count
    crud.increment_view_count(db=db, item_id=item_id)
    
    return item


@router.put("/{item_id}", response_model=schemas.ClothingItemResponse)
async def update_product(
    item_id: int,
    product_update: schemas.ClothingItemUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Update clothing item"""
    item = crud.update_clothing_item(db=db, item_id=item_id, item_update=product_update)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return item


@router.post("/search", response_model=List[schemas.ClothingItemResponse])
async def search_products(
    search_request: schemas.ProductSearchRequest,
    db: Session = Depends(get_db)
):
    """Search products with advanced filtering"""
    if search_request.query:
        items = crud.search_clothing_items(
            db=db,
            query=search_request.query,
            skip=(search_request.page - 1) * search_request.page_size,
            limit=search_request.page_size
        )
    else:
        items = crud.get_clothing_items(
            db=db,
            skip=(search_request.page - 1) * search_request.page_size,
            limit=search_request.page_size,
            category=search_request.category,
            brand=search_request.brand,
            min_price=search_request.min_price,
            max_price=search_request.max_price,
            ar_compatible=search_request.ar_compatible
        )
    
    return items


@router.post("/compare", response_model=List[schemas.ClothingItemResponse])
async def compare_products(
    item_ids: List[int],
    db: Session = Depends(get_db)
):
    """Compare multiple products"""
    items = []
    for item_id in item_ids:
        item = crud.get_clothing_item(db=db, item_id=item_id)
        if item:
            items.append(item)
    
    return items
