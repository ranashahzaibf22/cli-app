"""Style matching model for outfit compatibility"""
import numpy as np
from typing import List, Dict
import tensorflow as tf


class StyleMatcher:
    """
    Siamese network for style compatibility scoring
    Determines how well clothing items work together
    """
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.embedding_model = None
        
        if model_path:
            self.load_model(model_path)
    
    def build_embedding_network(self, input_shape=(224, 224, 3)):
        """Build embedding network for items"""
        inputs = tf.keras.Input(shape=input_shape)
        
        # Use MobileNetV2 for efficiency
        base = tf.keras.applications.MobileNetV2(
            input_shape=input_shape,
            include_top=False,
            weights='imagenet'
        )
        base.trainable = False
        
        x = base(inputs)
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = tf.keras.layers.Dense(256, activation='relu')(x)
        x = tf.keras.layers.Dropout(0.3)(x)
        embeddings = tf.keras.layers.Dense(128, activation=None)(x)
        
        # L2 normalize embeddings
        embeddings = tf.keras.layers.Lambda(
            lambda x: tf.math.l2_normalize(x, axis=1)
        )(embeddings)
        
        model = tf.keras.Model(inputs, embeddings)
        return model
    
    def build_compatibility_model(self):
        """Build full compatibility scoring model"""
        # Input for multiple items (up to 5)
        item_inputs = [
            tf.keras.Input(shape=(224, 224, 3), name=f'item_{i}')
            for i in range(5)
        ]
        
        # Shared embedding network
        self.embedding_model = self.build_embedding_network()
        
        # Get embeddings for all items
        embeddings = [self.embedding_model(item_input) for item_input in item_inputs]
        
        # Concatenate all embeddings
        combined = tf.keras.layers.Concatenate()(embeddings)
        
        # Compatibility scoring network
        x = tf.keras.layers.Dense(256, activation='relu')(combined)
        x = tf.keras.layers.Dropout(0.4)(x)
        x = tf.keras.layers.Dense(128, activation='relu')(x)
        x = tf.keras.layers.Dropout(0.3)(x)
        compatibility_score = tf.keras.layers.Dense(1, activation='sigmoid')(x)
        
        self.model = tf.keras.Model(item_inputs, compatibility_score)
        
        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return self.model
    
    def train(self, train_data, val_data, epochs=30):
        """Train the compatibility model"""
        if self.model is None:
            self.build_compatibility_model()
        
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
    
    def predict_compatibility(self, item_images: List[np.ndarray]) -> Dict:
        """Predict compatibility score for outfit"""
        if self.model is None:
            raise ValueError("Model not loaded or trained")
        
        # Pad to 5 items if needed
        while len(item_images) < 5:
            item_images.append(np.zeros((224, 224, 3)))
        
        # Preprocess images
        processed = []
        for img in item_images[:5]:
            if img.shape != (224, 224, 3):
                img = tf.image.resize(img, (224, 224))
            img = tf.cast(img, tf.float32) / 255.0
            processed.append(np.expand_dims(img, axis=0))
        
        # Predict
        score = self.model.predict(processed, verbose=0)[0][0]
        
        # Generate explanation based on score
        if score >= 0.8:
            explanation = "Excellent match! These items create a cohesive and stylish outfit."
            suggestions = []
        elif score >= 0.6:
            explanation = "Good combination with minor adjustments recommended."
            suggestions = ["Consider matching accessories", "Ensure color harmony"]
        else:
            explanation = "This combination may not work well together."
            suggestions = [
                "Try different color combinations",
                "Consider the occasion and style consistency",
                "Match formal/casual levels"
            ]
        
        return {
            'compatibility_score': float(score),
            'explanation': explanation,
            'suggestions': suggestions,
            'rating': 'excellent' if score >= 0.8 else 'good' if score >= 0.6 else 'needs_work'
        }
    
    def get_item_embedding(self, image: np.ndarray) -> np.ndarray:
        """Get embedding vector for single item"""
        if self.embedding_model is None:
            raise ValueError("Model not loaded or trained")
        
        # Preprocess
        if image.shape != (224, 224, 3):
            image = tf.image.resize(image, (224, 224))
        image = tf.cast(image, tf.float32) / 255.0
        image = np.expand_dims(image, axis=0)
        
        # Get embedding
        embedding = self.embedding_model.predict(image, verbose=0)[0]
        
        return embedding
    
    def find_similar_items(
        self,
        query_image: np.ndarray,
        item_database: List[np.ndarray],
        top_k: int = 5
    ) -> List[Dict]:
        """Find similar items using embedding similarity"""
        query_emb = self.get_item_embedding(query_image)
        
        similarities = []
        for i, item_img in enumerate(item_database):
            item_emb = self.get_item_embedding(item_img)
            # Cosine similarity (embeddings are already normalized)
            similarity = np.dot(query_emb, item_emb)
            similarities.append({
                'index': i,
                'similarity': float(similarity)
            })
        
        # Sort by similarity
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        return similarities[:top_k]
    
    def save_model(self, path_prefix: str):
        """Save models"""
        if self.model is None:
            raise ValueError("No model to save")
        
        self.model.save(f"{path_prefix}_full.h5")
        self.embedding_model.save(f"{path_prefix}_embedding.h5")
    
    def load_model(self, path_prefix: str):
        """Load models"""
        self.model = tf.keras.models.load_model(f"{path_prefix}_full.h5")
        self.embedding_model = tf.keras.models.load_model(f"{path_prefix}_embedding.h5")
