"""Fashion classifier using CNN"""
import numpy as np
from typing import Dict, List
import tensorflow as tf


class FashionClassifier:
    """
    CNN-based fashion item classifier
    Categories: shirts, pants, dresses, outerwear, shoes, accessories
    """
    
    def __init__(self, model_path: str = None):
        self.categories = ['shirts', 'pants', 'dresses', 'outerwear', 'shoes', 'accessories']
        self.model = None
        
        if model_path:
            self.load_model(model_path)
    
    def build_model(self, input_shape=(224, 224, 3)):
        """Build ResNet50-based classifier"""
        base_model = tf.keras.applications.ResNet50(
            weights='imagenet',
            include_top=False,
            input_shape=input_shape
        )
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Add custom classification head
        inputs = tf.keras.Input(shape=input_shape)
        x = base_model(inputs, training=False)
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = tf.keras.layers.Dense(256, activation='relu')(x)
        x = tf.keras.layers.Dropout(0.5)(x)
        outputs = tf.keras.layers.Dense(len(self.categories), activation='softmax')(x)
        
        self.model = tf.keras.Model(inputs, outputs)
        
        # Compile model
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return self.model
    
    def train(self, train_data, val_data, epochs=50):
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
