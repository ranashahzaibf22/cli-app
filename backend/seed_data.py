"""Seed database with initial data"""
import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal
from app.models import Base, User, ClothingItem, ARSession, MLModel
from app.auth import get_password_hash


def load_fashion_items():
    """Load fashion items from JSON file"""
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'datasets', 'fashion_items.json')
    
    if not os.path.exists(json_path):
        print(f"Fashion items file not found: {json_path}")
        return []
    
    with open(json_path, 'r') as f:
        items = json.load(f)
    
    return items


def seed_database():
    """Seed the database with initial data"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"Database already has {existing_users} users. Skipping seed.")
            return
        
        print("Seeding database...")
        
        # Create test users
        print("Creating test users...")
        users = [
            User(
                email="admin@stylesense.ai",
                username="admin",
                password_hash=get_password_hash("admin123"),
                full_name="Admin User",
                body_measurements={
                    "height": 70,
                    "weight": 170,
                    "chest": 40,
                    "waist": 34,
                    "hips": 40,
                    "inseam": 32,
                    "shoulder_width": 18
                },
                style_preferences={
                    "colors": ["navy", "gray", "black"],
                    "styles": ["business-casual", "minimalist"],
                    "occasions": ["work", "casual"],
                    "brands": ["Gap", "J.Crew", "Banana Republic"]
                }
            ),
            User(
                email="test@example.com",
                username="testuser",
                password_hash=get_password_hash("password123"),
                full_name="Test User",
                body_measurements={
                    "height": 68,
                    "weight": 160,
                    "chest": 38,
                    "waist": 32,
                    "hips": 38,
                    "inseam": 30,
                    "shoulder_width": 17
                },
                style_preferences={
                    "colors": ["blue", "white", "khaki"],
                    "styles": ["casual", "athletic"],
                    "occasions": ["casual", "outdoor"],
                    "brands": ["Nike", "Levi's", "Uniqlo"]
                }
            ),
            User(
                email="jane@example.com",
                username="jane_doe",
                password_hash=get_password_hash("jane123"),
                full_name="Jane Doe",
                body_measurements={
                    "height": 65,
                    "weight": 130,
                    "chest": 34,
                    "waist": 27,
                    "hips": 37,
                    "inseam": 28,
                    "shoulder_width": 15
                },
                style_preferences={
                    "colors": ["pink", "white", "beige"],
                    "styles": ["elegant", "casual", "romantic"],
                    "occasions": ["work", "evening", "casual"],
                    "brands": ["Zara", "Mango", "Free People"]
                }
            )
        ]
        
        for user in users:
            db.add(user)
        
        db.commit()
        print(f"Created {len(users)} test users")
        
        # Load and create clothing items
        print("Loading clothing items...")
        fashion_items = load_fashion_items()
        
        if not fashion_items:
            print("No fashion items to load!")
            return
        
        print(f"Creating {len(fashion_items)} clothing items...")
        for item_data in fashion_items:
            # Convert to ClothingItem model
            item = ClothingItem(
                name=item_data['name'],
                description=item_data['description'],
                category=item_data['category'],
                subcategory=item_data.get('category', ''),  # Use category as subcategory
                brand=item_data['brand'],
                price=item_data['price'],
                image_urls=[item_data['image_url']],
                color_variants=item_data.get('colors', []),
                size_chart=item_data.get('size_chart', {}),
                materials=["Cotton Blend"],  # Default material
                care_instructions="Machine wash cold",
                sustainability_score=75,  # Default score
                ar_compatible=item_data.get('ar_compatible', True),
                ml_features={
                    "style_tags": item_data.get('style_tags', []),
                    "colors": item_data.get('colors', []),
                    "price_range": "mid" if 50 <= item_data['price'] <= 150 else ("high" if item_data['price'] > 150 else "low")
                },
                view_count=0,
                try_on_count=0
            )
            db.add(item)
        
        db.commit()
        print(f"Created {len(fashion_items)} clothing items")
        
        # Create ML model records
        print("Creating ML model records...")
        ml_models = [
            MLModel(
                model_name="Fashion Classifier",
                model_type="classification",
                version="1.0",
                file_path="ml_models/models/fashion_classifier.pkl",
                training_data_size=240,
                accuracy_metrics={
                    "accuracy": 0.92,
                    "precision": 0.91,
                    "recall": 0.90
                },
                performance_metrics={
                    "inference_time_ms": 50,
                    "memory_mb": 25
                },
                training_date=datetime.utcnow(),
                status="ready",
                description="Random Forest classifier for fashion item categorization"
            ),
            MLModel(
                model_name="Size Recommender",
                model_type="recommendation",
                version="1.0",
                file_path="ml_models/models/size_recommender.pkl",
                training_data_size=150,
                accuracy_metrics={
                    "accuracy": 0.87,
                    "mae": 0.5
                },
                performance_metrics={
                    "inference_time_ms": 30,
                    "memory_mb": 15
                },
                training_date=datetime.utcnow(),
                status="ready",
                description="Rule-based size recommendation system"
            ),
            MLModel(
                model_name="Style Matcher",
                model_type="similarity",
                version="1.0",
                file_path="ml_models/models/style_matcher.pkl",
                training_data_size=200,
                accuracy_metrics={
                    "agreement_score": 0.83,
                    "top5_accuracy": 0.95
                },
                performance_metrics={
                    "inference_time_ms": 60,
                    "memory_mb": 40
                },
                training_date=datetime.utcnow(),
                status="ready",
                description="Style compatibility matcher for outfit recommendations"
            ),
            MLModel(
                model_name="User Preference Model",
                model_type="recommendation",
                version="1.0",
                file_path="ml_models/models/user_preference.pkl",
                training_data_size=500,
                accuracy_metrics={
                    "ndcg": 0.78,
                    "map": 0.72
                },
                performance_metrics={
                    "inference_time_ms": 80,
                    "memory_mb": 50
                },
                training_date=datetime.utcnow(),
                status="ready",
                description="Personalized recommendation engine"
            )
        ]
        
        for model in ml_models:
            db.add(model)
        
        db.commit()
        print(f"Created {len(ml_models)} ML model records")
        
        # Create sample AR sessions
        print("Creating sample AR sessions...")
        sample_sessions = [
            ARSession(
                user_id=users[1].id,
                clothing_item_id=1,
                session_type="photo",
                pose_landmarks={},
                body_measurements_detected={
                    "chest": 38,
                    "waist": 32,
                    "shoulder_width": 17
                },
                fit_analysis={
                    "fit_score": 0.85,
                    "fit_assessment": "Good Fit",
                    "recommendations": ["Size M recommended"]
                },
                quality_score=0.90,
                processing_time=3.2,
                ar_metadata={"lighting": "good", "pose_quality": "excellent"}
            ),
            ARSession(
                user_id=users[2].id,
                clothing_item_id=21,
                session_type="photo",
                pose_landmarks={},
                body_measurements_detected={
                    "chest": 34,
                    "waist": 27,
                    "hips": 37
                },
                fit_analysis={
                    "fit_score": 0.92,
                    "fit_assessment": "Excellent Fit",
                    "recommendations": ["Size S is perfect"]
                },
                quality_score=0.95,
                processing_time=2.8,
                ar_metadata={"lighting": "excellent", "pose_quality": "good"}
            )
        ]
        
        for session in sample_sessions:
            db.add(session)
        
        db.commit()
        print(f"Created {len(sample_sessions)} sample AR sessions")
        
        print("\n✅ Database seeded successfully!")
        print(f"   - Users: {len(users)}")
        print(f"   - Clothing Items: {len(fashion_items)}")
        print(f"   - ML Models: {len(ml_models)}")
        print(f"   - AR Sessions: {len(sample_sessions)}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
