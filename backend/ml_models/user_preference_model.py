"""User preference learning using collaborative filtering"""
import numpy as np
from typing import List, Dict, Tuple
from sklearn.decomposition import NMF
import tensorflow as tf


class UserPreferenceModel:
    """
    Personalized recommendation using matrix factorization and deep learning
    Combines collaborative filtering with content-based features
    """
    
    def __init__(self, n_users: int = 1000, n_items: int = 500, n_factors: int = 50):
        self.n_users = n_users
        self.n_items = n_items
        self.n_factors = n_factors
        
        self.nmf_model = None
        self.dl_model = None
        
        self.user_factors = None
        self.item_factors = None
    
    def build_nmf_model(self):
        """Build Non-negative Matrix Factorization model"""
        self.nmf_model = NMF(
            n_components=self.n_factors,
            init='random',
            random_state=42,
            max_iter=500
        )
        return self.nmf_model
    
    def build_deep_learning_model(self, n_item_features: int = 20):
        """Build deep learning model for recommendations"""
        # User input
        user_input = tf.keras.Input(shape=(1,), name='user_id')
        user_embedding = tf.keras.layers.Embedding(
            self.n_users,
            self.n_factors,
            name='user_embedding'
        )(user_input)
        user_embedding = tf.keras.layers.Flatten()(user_embedding)
        
        # Item input
        item_input = tf.keras.Input(shape=(1,), name='item_id')
        item_embedding = tf.keras.layers.Embedding(
            self.n_items,
            self.n_factors,
            name='item_embedding'
        )(item_input)
        item_embedding = tf.keras.layers.Flatten()(item_embedding)
        
        # Item features input
        item_features = tf.keras.Input(shape=(n_item_features,), name='item_features')
        
        # Concatenate all inputs
        concat = tf.keras.layers.Concatenate()([
            user_embedding,
            item_embedding,
            item_features
        ])
        
        # Deep network
        x = tf.keras.layers.Dense(128, activation='relu')(concat)
        x = tf.keras.layers.Dropout(0.3)(x)
        x = tf.keras.layers.Dense(64, activation='relu')(x)
        x = tf.keras.layers.Dropout(0.2)(x)
        x = tf.keras.layers.Dense(32, activation='relu')(x)
        
        # Output: predicted rating/preference
        output = tf.keras.layers.Dense(1, activation='sigmoid')(x)
        
        self.dl_model = tf.keras.Model(
            inputs=[user_input, item_input, item_features],
            outputs=output
        )
        
        self.dl_model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        return self.dl_model
    
    def train_nmf(self, user_item_matrix: np.ndarray):
        """Train NMF model on user-item interaction matrix"""
        if self.nmf_model is None:
            self.build_nmf_model()
        
        # Fit NMF
        self.user_factors = self.nmf_model.fit_transform(user_item_matrix)
        self.item_factors = self.nmf_model.components_.T
        
        # Reconstruction error
        reconstructed = np.dot(self.user_factors, self.item_factors.T)
        error = np.mean((user_item_matrix - reconstructed) ** 2)
        
        return {
            'reconstruction_error': error,
            'user_factors_shape': self.user_factors.shape,
            'item_factors_shape': self.item_factors.shape
        }
    
    def train_deep_model(
        self,
        train_data: Tuple[Dict, np.ndarray],
        val_data: Tuple[Dict, np.ndarray],
        epochs: int = 30
    ):
        """Train deep learning model"""
        if self.dl_model is None:
            # Infer item features dimension from data
            n_features = train_data[0]['item_features'].shape[1]
            self.build_deep_learning_model(n_item_features=n_features)
        
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3
            )
        ]
        
        history = self.dl_model.fit(
            train_data[0],
            train_data[1],
            validation_data=val_data,
            epochs=epochs,
            batch_size=256,
            callbacks=callbacks,
            verbose=0
        )
        
        return history
    
    def predict_preference(
        self,
        user_id: int,
        item_id: int,
        item_features: np.ndarray,
        use_dl: bool = True
    ) -> float:
        """Predict user preference for item"""
        if use_dl and self.dl_model is not None:
            # Use deep learning model
            prediction = self.dl_model.predict(
                {
                    'user_id': np.array([user_id]),
                    'item_id': np.array([item_id]),
                    'item_features': item_features.reshape(1, -1)
                },
                verbose=0
            )[0][0]
        elif self.user_factors is not None and self.item_factors is not None:
            # Use NMF
            prediction = np.dot(self.user_factors[user_id], self.item_factors[item_id])
            # Normalize to [0, 1]
            prediction = max(0, min(1, prediction / 5.0))
        else:
            raise ValueError("No model trained")
        
        return float(prediction)
    
    def recommend_items(
        self,
        user_id: int,
        item_features_list: List[np.ndarray],
        n_recommendations: int = 10,
        exclude_items: List[int] = None
    ) -> List[Dict]:
        """Generate personalized recommendations for user"""
        if exclude_items is None:
            exclude_items = []
        
        recommendations = []
        
        for item_id, item_features in enumerate(item_features_list):
            if item_id in exclude_items:
                continue
            
            # Get preference score
            score = self.predict_preference(user_id, item_id, item_features)
            
            recommendations.append({
                'item_id': item_id,
                'score': score
            })
        
        # Sort by score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return recommendations[:n_recommendations]
    
    def get_similar_users(self, user_id: int, top_k: int = 10) -> List[Dict]:
        """Find similar users based on preference patterns"""
        if self.user_factors is None:
            raise ValueError("NMF model not trained")
        
        user_vector = self.user_factors[user_id]
        
        # Compute cosine similarity with all users
        similarities = []
        for other_id in range(self.n_users):
            if other_id == user_id:
                continue
            
            other_vector = self.user_factors[other_id]
            
            # Cosine similarity
            similarity = np.dot(user_vector, other_vector) / (
                np.linalg.norm(user_vector) * np.linalg.norm(other_vector) + 1e-8
            )
            
            similarities.append({
                'user_id': other_id,
                'similarity': float(similarity)
            })
        
        # Sort by similarity
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        return similarities[:top_k]
    
    def explain_recommendation(
        self,
        user_id: int,
        item_id: int,
        item_features: np.ndarray
    ) -> str:
        """Generate explanation for recommendation"""
        score = self.predict_preference(user_id, item_id, item_features)
        
        if score >= 0.8:
            explanation = "Highly recommended based on your preferences and browsing history."
        elif score >= 0.6:
            explanation = "This item matches some of your interests and style preferences."
        elif score >= 0.4:
            explanation = "This item might interest you based on similar users' preferences."
        else:
            explanation = "This is a popular item that other users enjoy."
        
        return explanation
    
    def save_models(self, path_prefix: str):
        """Save models"""
        # Save NMF factors
        if self.user_factors is not None:
            np.save(f"{path_prefix}_user_factors.npy", self.user_factors)
            np.save(f"{path_prefix}_item_factors.npy", self.item_factors)
        
        # Save DL model
        if self.dl_model is not None:
            self.dl_model.save(f"{path_prefix}_dl_model.h5")
    
    def load_models(self, path_prefix: str):
        """Load models"""
        try:
            self.user_factors = np.load(f"{path_prefix}_user_factors.npy")
            self.item_factors = np.load(f"{path_prefix}_item_factors.npy")
        except FileNotFoundError:
            pass
        
        try:
            self.dl_model = tf.keras.models.load_model(f"{path_prefix}_dl_model.h5")
        except (FileNotFoundError, OSError):
            pass
