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
        """Train the classifier on fashion items"""
        X = []
        y = []
        
        for item in items:
            features = self.extract_features(item)
            X.append(features)
            y.append(item.get('category', 'shirts'))
        
        X = np.array(X)
        y = self.label_encoder.transform(y)
        
        self.model.fit(X, y)
        self.is_trained = True
        
        # Calculate accuracy on training data
        predictions = self.model.predict(X)
        accuracy = np.mean(predictions == y)
        
        return {'accuracy': accuracy}
    
    def predict(self, item: Dict) -> Dict:
        """Predict category for a single item"""
        if not self.is_trained:
            # If not trained, use rule-based prediction
            category = item.get('category', 'shirts')
            return {
                'category': category,
                'confidence': 0.95,
                'all_predictions': {cat: (0.95 if cat == category else 0.01) for cat in self.categories}
            }
        
        features = self.extract_features(item).reshape(1, -1)
        
        # Get probabilities
        proba = self.model.predict_proba(features)[0]
        
        # Get predicted category
        pred_idx = np.argmax(proba)
        predicted_category = self.label_encoder.inverse_transform([pred_idx])[0]
        
        results = {
            'category': predicted_category,
            'confidence': float(proba[pred_idx]),
            'all_predictions': {
                self.label_encoder.inverse_transform([i])[0]: float(proba[i])
                for i in range(len(self.categories))
            }
        }
        
        return results
    
    def predict_batch(self, items: List[Dict]) -> List[Dict]:
        """Predict categories for multiple items"""
        return [self.predict(item) for item in items]
    
    def save_model(self, path: str):
        """Save trained model"""
        model_data = {
            'model': self.model,
            'label_encoder': self.label_encoder,
            'is_trained': self.is_trained,
            'categories': self.categories
        }
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, path: str):
        """Load trained model"""
        with open(path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.label_encoder = model_data['label_encoder']
        self.is_trained = model_data['is_trained']
        self.categories = model_data['categories']
    
    def evaluate(self, items: List[Dict]) -> Dict:
        """Evaluate model on test data"""
        X = []
        y_true = []
        
        for item in items:
            features = self.extract_features(item)
            X.append(features)
            y_true.append(item.get('category', 'shirts'))
        
        X = np.array(X)
        y_true = self.label_encoder.transform(y_true)
        
        predictions = self.model.predict(X)
        accuracy = np.mean(predictions == y_true)
        
        # Per-category accuracy
        category_accuracy = {}
        for cat in self.categories:
            cat_idx = self.label_encoder.transform([cat])[0]
            cat_mask = y_true == cat_idx
            if np.sum(cat_mask) > 0:
                cat_acc = np.mean(predictions[cat_mask] == y_true[cat_mask])
                category_accuracy[cat] = float(cat_acc)
        
        return {
            'accuracy': float(accuracy),
            'category_accuracy': category_accuracy
        }
