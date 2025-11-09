"""Size recommendation model"""
import numpy as np
from typing import Dict, List, Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import pickle


class SizeRecommender:
    """
    Ensemble model for size recommendation
    Combines Random Forest and Neural Network
    """
    
    def __init__(self):
        self.sizes = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL']
        self.rf_model = None
        self.nn_model = None
        self.scaler = StandardScaler()
        
        # Feature names
        self.user_features = ['height', 'weight', 'chest', 'waist', 'hips', 'inseam', 'shoulder_width']
        self.item_features = ['brand_id', 'category_id', 'fit_type', 'stretch_factor', 'size_run']
    
    def build_rf_model(self):
        """Build Random Forest classifier"""
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        return self.rf_model
    
    def build_nn_model(self, input_dim=12):
        """Build Neural Network classifier"""
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_dim=input_dim),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(len(self.sizes), activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.nn_model = model
        return model
    
    def prepare_features(self, user_measurements: Dict, item_specs: Dict) -> np.ndarray:
        """Prepare feature vector from user and item data"""
        user_vals = [user_measurements.get(f, 0) for f in self.user_features]
        item_vals = [item_specs.get(f, 0) for f in self.item_features]
        
        features = np.array(user_vals + item_vals).reshape(1, -1)
        return features
    
    def train(self, X_train, y_train, X_val, y_val):
        """Train both models"""
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        
        # Train Random Forest
        print("Training Random Forest...")
        self.build_rf_model()
        self.rf_model.fit(X_train_scaled, y_train)
        rf_val_acc = self.rf_model.score(X_val_scaled, y_val)
        print(f"RF Validation Accuracy: {rf_val_acc:.4f}")
        
        # Train Neural Network
        print("Training Neural Network...")
        self.build_nn_model(input_dim=X_train.shape[1])
        
        # Convert labels to categorical
        y_train_cat = tf.keras.utils.to_categorical(y_train, len(self.sizes))
        y_val_cat = tf.keras.utils.to_categorical(y_val, len(self.sizes))
        
        history = self.nn_model.fit(
            X_train_scaled, y_train_cat,
            validation_data=(X_val_scaled, y_val_cat),
            epochs=30,
            batch_size=32,
            verbose=0
        )
        
        nn_val_acc = max(history.history['val_accuracy'])
        print(f"NN Validation Accuracy: {nn_val_acc:.4f}")
        
        return {
            'rf_accuracy': rf_val_acc,
            'nn_accuracy': nn_val_acc
        }
    
    def predict(self, user_measurements: Dict, item_specs: Dict) -> Dict:
        """Predict size using ensemble"""
        if self.rf_model is None or self.nn_model is None:
            raise ValueError("Models not trained")
        
        # Prepare features
        features = self.prepare_features(user_measurements, item_specs)
        features_scaled = self.scaler.transform(features)
        
        # Get predictions from both models
        rf_probs = self.rf_model.predict_proba(features_scaled)[0]
        nn_probs = self.nn_model.predict(features_scaled, verbose=0)[0]
        
        # Ensemble: weighted average (70% RF, 30% NN)
        ensemble_probs = 0.7 * rf_probs + 0.3 * nn_probs
        
        # Get top prediction
        top_idx = np.argmax(ensemble_probs)
        recommended_size = self.sizes[top_idx]
        confidence = ensemble_probs[top_idx]
        
        # Get alternative sizes
        sorted_indices = np.argsort(ensemble_probs)[::-1]
        alternatives = [
            {
                'size': self.sizes[i],
                'confidence': float(ensemble_probs[i])
            }
            for i in sorted_indices[1:4]  # Top 3 alternatives
        ]
        
        return {
            'recommended_size': recommended_size,
            'confidence_score': float(confidence),
            'alternative_sizes': alternatives,
            'model_breakdown': {
                'rf_prediction': self.sizes[np.argmax(rf_probs)],
                'nn_prediction': self.sizes[np.argmax(nn_probs)]
            }
        }
    
    def save(self, path_prefix: str):
        """Save models"""
        # Save RF model
        with open(f"{path_prefix}_rf.pkl", 'wb') as f:
            pickle.dump(self.rf_model, f)
        
        # Save NN model
        self.nn_model.save(f"{path_prefix}_nn.h5")
        
        # Save scaler
        with open(f"{path_prefix}_scaler.pkl", 'wb') as f:
            pickle.dump(self.scaler, f)
    
    def load(self, path_prefix: str):
        """Load models"""
        # Load RF model
        with open(f"{path_prefix}_rf.pkl", 'rb') as f:
            self.rf_model = pickle.load(f)
        
        # Load NN model
        self.nn_model = tf.keras.models.load_model(f"{path_prefix}_nn.h5")
        
        # Load scaler
        with open(f"{path_prefix}_scaler.pkl", 'rb') as f:
            self.scaler = pickle.load(f)
