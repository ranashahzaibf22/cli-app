"""Fashion classifier using simple machine learning"""
import numpy as np
from typing import Dict, List
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


class FashionClassifier:
    """
    Simple ML-based fashion item classifier using product attributes
    Categories: shirts, pants, dresses, jackets, shoes, accessories
    """
    
    def __init__(self, model_path: str = None):
        self.categories = ['shirts', 'pants', 'dresses', 'jackets', 'shoes', 'accessories']
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(self.categories)
        self.is_trained = False
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def extract_features(self, item: Dict) -> np.ndarray:
        """Extract features from item attributes"""
        features = []
        
        # Price range feature (normalized)
        price = item.get('price', 50.0)
        features.append(min(price / 500.0, 1.0))  # Normalize to 0-1
        
        # Brand encoding (simple hash)
        brand = item.get('brand', '')
        features.append(hash(brand) % 100 / 100.0)
        
        # Style tags features (binary)
        all_tags = ['casual', 'formal', 'sporty', 'elegant', 'vintage', 'trendy']
        item_tags = item.get('style_tags', [])
        for tag in all_tags:
            features.append(1.0 if tag in item_tags else 0.0)
        
        # AR compatible
        features.append(1.0 if item.get('ar_compatible', False) else 0.0)
        
        # Number of sizes
        sizes = item.get('sizes_available', [])
        features.append(len(sizes) / 10.0)  # Normalize
        
        return np.array(features)
    
    def train(self, items: List[Dict]):
        """Train the model"""
        if self.model is None:
            self.build_model()
        
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=5,
                restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3
            )
        ]
        
        history = self.model.fit(
            train_data,
            validation_data=val_data,
            epochs=epochs,
            callbacks=callbacks
        )
        
        return history
    
    def predict(self, image: np.ndarray) -> Dict:
        """Predict category for single image"""
        if self.model is None:
            raise ValueError("Model not loaded or trained")
        
        # Preprocess image
        if image.shape != (224, 224, 3):
            image = tf.image.resize(image, (224, 224))
        
        image = tf.cast(image, tf.float32) / 255.0
        image = np.expand_dims(image, axis=0)
        
        # Predict
        predictions = self.model.predict(image)[0]
        
        # Get top predictions
        top_idx = np.argsort(predictions)[::-1]
        
        results = {
            'category': self.categories[top_idx[0]],
            'confidence': float(predictions[top_idx[0]]),
            'all_predictions': {
                self.categories[i]: float(predictions[i])
                for i in range(len(self.categories))
            }
        }
        
        return results
    
    def save_model(self, path: str):
        """Save trained model"""
        if self.model is None:
            raise ValueError("No model to save")
        
        self.model.save(path)
    
    def load_model(self, path: str):
        """Load trained model"""
        self.model = tf.keras.models.load_model(path)
    
    def evaluate(self, test_data):
        """Evaluate model on test data"""
        if self.model is None:
            raise ValueError("Model not loaded or trained")
        
        results = self.model.evaluate(test_data)
        
        return {
            'loss': results[0],
            'accuracy': results[1]
        }
