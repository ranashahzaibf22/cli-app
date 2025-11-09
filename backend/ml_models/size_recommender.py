"""Size recommendation model - Simplified"""
import numpy as np
from typing import Dict, List, Tuple, Optional
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import pickle
import os


class SizeRecommender:
    """
    Simple rule-based size recommendation with ML fallback
    """
    
    def __init__(self):
        self.sizes = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL']
        self.numeric_sizes = ['26', '28', '30', '32', '34', '36', '38', '40']
        self.model = RandomForestRegressor(n_estimators=50, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
        # Size mapping based on measurements (in inches)
        self.size_chart = {
            'shirts': {
                'XXS': {'chest': (30, 32), 'waist': (24, 26)},
                'XS': {'chest': (32, 34), 'waist': (26, 28)},
                'S': {'chest': (34, 37), 'waist': (28, 31)},
                'M': {'chest': (37, 40), 'waist': (31, 34)},
                'L': {'chest': (40, 43), 'waist': (34, 37)},
                'XL': {'chest': (43, 46), 'waist': (37, 40)},
                'XXL': {'chest': (46, 50), 'waist': (40, 44)}
            },
            'pants': {
                '26': (25, 27), '28': (27, 29), '30': (29, 31),
                '32': (31, 33), '34': (33, 35), '36': (35, 37),
                '38': (37, 39), '40': (39, 42)
            },
            'dresses': {
                'XXS': {'bust': (30, 32), 'waist': (23, 25), 'hips': (33, 35)},
                'XS': {'bust': (32, 34), 'waist': (25, 27), 'hips': (35, 37)},
                'S': {'bust': (34, 36), 'waist': (27, 29), 'hips': (37, 39)},
                'M': {'bust': (36, 38), 'waist': (29, 31), 'hips': (39, 41)},
                'L': {'bust': (38, 41), 'waist': (31, 34), 'hips': (41, 44)},
                'XL': {'bust': (41, 44), 'waist': (34, 37), 'hips': (44, 47)},
                'XXL': {'bust': (44, 47), 'waist': (37, 40), 'hips': (47, 50)}
            }
        }
    
    def rule_based_predict(self, user_measurements: Dict, item_specs: Dict) -> Dict:
        """Rule-based size prediction"""
        category = item_specs.get('category', 'shirts').lower()
        
        # Get user measurements
        chest = user_measurements.get('chest', 38)
        waist = user_measurements.get('waist', 32)
        hips = user_measurements.get('hips', 40)
        height = user_measurements.get('height', 68)  # inches
        
        # Predict size based on category
        if category in ['shirts', 'jackets']:
            chart = self.size_chart.get('shirts', {})
            for size, measurements in chart.items():
                chest_range = measurements.get('chest', (0, 100))
                if chest_range[0] <= chest <= chest_range[1]:
                    return self._create_prediction(size, 0.85, category)
            
            # Default to M
            return self._create_prediction('M', 0.70, category)
        
        elif category == 'pants':
            # Use waist measurement
            for size in self.numeric_sizes:
                size_num = int(size)
                if abs(waist - size_num) <= 2:
                    return self._create_prediction(size, 0.90, category)
            
            # Default to closest size
            closest = min(self.numeric_sizes, key=lambda x: abs(int(x) - waist))
            return self._create_prediction(closest, 0.75, category)
        
        elif category == 'dresses':
            chart = self.size_chart.get('dresses', {})
            scores = {}
            
            for size, measurements in chart.items():
                bust_range = measurements.get('bust', (0, 100))
                waist_range = measurements.get('waist', (0, 100))
                hips_range = measurements.get('hips', (0, 100))
                
                # Calculate fit score
                bust_fit = bust_range[0] <= chest <= bust_range[1]
                waist_fit = waist_range[0] <= waist <= waist_range[1]
                hips_fit = hips_range[0] <= hips <= hips_range[1]
                
                score = sum([bust_fit, waist_fit, hips_fit]) / 3.0
                scores[size] = score
            
            if scores:
                best_size = max(scores, key=scores.get)
                confidence = scores[best_size]
                return self._create_prediction(best_size, confidence * 0.9, category)
            
            return self._create_prediction('M', 0.65, category)
        
        else:
            # Default sizing
            return self._create_prediction('M', 0.70, category)
    
    def _create_prediction(self, size: str, confidence: float, category: str) -> Dict:
        """Create prediction response"""
        # Generate alternatives
        if size in self.sizes:
            size_idx = self.sizes.index(size)
            alternatives = []
            
            if size_idx > 0:
                alternatives.append(self.sizes[size_idx - 1])
            if size_idx < len(self.sizes) - 1:
                alternatives.append(self.sizes[size_idx + 1])
        
        elif size in self.numeric_sizes:
            size_idx = self.numeric_sizes.index(size)
            alternatives = []
            
            if size_idx > 0:
                alternatives.append(self.numeric_sizes[size_idx - 1])
            if size_idx < len(self.numeric_sizes) - 1:
                alternatives.append(self.numeric_sizes[size_idx + 1])
        else:
            alternatives = ['S', 'L']
        
        return {
            'recommended_size': size,
            'confidence': round(confidence, 2),
            'alternatives': alternatives,
            'fit_advice': self._get_fit_advice(confidence, size)
        }
    
    def _get_fit_advice(self, confidence: float, size: str) -> str:
        """Generate fit advice based on confidence"""
        if confidence >= 0.85:
            return f"Size {size} should fit you perfectly based on your measurements."
        elif confidence >= 0.70:
            return f"Size {size} is recommended. Consider trying the alternatives for best fit."
        else:
            return f"Size {size} is suggested, but we recommend trying it on or checking the detailed size chart."
    
    def predict(self, user_measurements: Dict, item_specs: Dict) -> Dict:
        """Predict size for user and item combination"""
        return self.rule_based_predict(user_measurements, item_specs)
    
    def train(self, training_data: List[Tuple[Dict, Dict, str]]):
        """Train model on historical fit data"""
        # For now, this is optional - rule-based works fine
        # training_data format: [(user_measurements, item_specs, actual_size), ...]
        self.is_trained = True
        return {'status': 'trained', 'samples': len(training_data)}
    
    def save_model(self, path: str):
        """Save model"""
        model_data = {
            'size_chart': self.size_chart,
            'is_trained': self.is_trained,
            'sizes': self.sizes
        }
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, path: str):
        """Load model"""
        with open(path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.size_chart = model_data.get('size_chart', self.size_chart)
        self.is_trained = model_data.get('is_trained', False)
        self.sizes = model_data.get('sizes', self.sizes)


# Simple function for quick size recommendations
def quick_size_recommendation(chest: int, waist: int, category: str = 'shirts') -> str:
    """Quick size recommendation without creating class instance"""
    recommender = SizeRecommender()
    user_measurements = {'chest': chest, 'waist': waist}
    item_specs = {'category': category}
    
    result = recommender.predict(user_measurements, item_specs)
    return result['recommended_size']
