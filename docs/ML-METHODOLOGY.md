# Machine Learning Methodology

## Overview

This document details the machine learning approaches, algorithms, and training methodologies used in the StyleSense.AI platform. Four custom models were developed to address specific fashion e-commerce challenges.

## 1. Fashion Item Classifier

### Problem Statement
Automatically categorize fashion items into predefined categories to enable efficient search and filtering.

### Architecture

**Model Type:** Convolutional Neural Network (CNN)  
**Base Architecture:** ResNet50  
**Transfer Learning:** Yes (ImageNet pre-trained weights)

```
Input (224x224x3)
    ↓
ResNet50 Base (frozen)
    ↓
Global Average Pooling
    ↓
Dense (256, ReLU)
    ↓
Dropout (0.5)
    ↓
Dense (6, Softmax)
    ↓
Output: [shirts, pants, dresses, outerwear, shoes, accessories]
```

### Training Methodology

**Dataset:**
- Training: 1,400 images (70%)
- Validation: 300 images (15%)
- Test: 300 images (15%)
- Stratified sampling to ensure balanced categories

**Data Augmentation:**
```python
augmentation = {
    'rotation_range': 15,
    'horizontal_flip': True,
    'brightness_range': [0.8, 1.2],
    'contrast_range': [0.8, 1.2],
    'zoom_range': [0.9, 1.1],
    'shear_range': 0.1
}
```

**Training Configuration:**
- Optimizer: Adam (lr=0.0001)
- Loss: Categorical Cross-Entropy
- Batch Size: 32
- Epochs: 50 (with early stopping)
- Callbacks: EarlyStopping (patience=5), ReduceLROnPlateau (patience=3)

**Hyperparameter Tuning:**
Tried learning rates: [0.001, 0.0001, 0.00001]  
Best: 0.0001

Tried dropout rates: [0.3, 0.5, 0.7]  
Best: 0.5

### Results

| Metric | Value |
|--------|-------|
| Test Accuracy | 92.3% |
| Precision (macro) | 91.8% |
| Recall (macro) | 91.5% |
| F1-Score (macro) | 91.6% |
| Training Time | 3.2 hours |
| Inference Time | 45ms |

**Per-Category Performance:**

| Category | Precision | Recall | F1-Score | Support |
|----------|-----------|--------|----------|---------|
| Shirts | 0.93 | 0.91 | 0.92 | 50 |
| Pants | 0.94 | 0.92 | 0.93 | 50 |
| Dresses | 0.96 | 0.94 | 0.95 | 50 |
| Outerwear | 0.90 | 0.91 | 0.90 | 50 |
| Shoes | 0.92 | 0.93 | 0.92 | 50 |
| Accessories | 0.86 | 0.88 | 0.87 | 50 |

### Error Analysis

**Common Misclassifications:**
1. Dresses vs Long Shirts: 8 cases (flowing designs)
2. Shoes vs Accessories: 5 cases (small accessories)
3. Outerwear vs Shirts: 4 cases (light jackets)

**Improvement Strategies:**
- Increase training data for ambiguous cases
- Add subcategory classification
- Incorporate style attributes in decision

---

## 2. Size Recommender

### Problem Statement
Predict appropriate clothing size based on user body measurements and item specifications.

### Architecture

**Model Type:** Ensemble (Random Forest + Neural Network)  
**Approach:** Weighted average of predictions

**Random Forest Component:**
```
Parameters:
- n_estimators: 100
- max_depth: 15
- min_samples_split: 5
- min_samples_leaf: 2
- Criterion: Gini
```

**Neural Network Component:**
```
Input (12 features)
    ↓
Dense (64, ReLU)
    ↓
Dropout (0.3)
    ↓
Dense (32, ReLU)
    ↓
Dropout (0.2)
    ↓
Dense (16, ReLU)
    ↓
Dense (7, Softmax)
    ↓
Output: Size probability distribution
```

**Ensemble Strategy:**
```
Final Prediction = 0.7 * RF_Prediction + 0.3 * NN_Prediction
```

### Feature Engineering

**User Measurements (7 features):**
1. Height (cm)
2. Weight (kg)
3. Chest circumference (cm)
4. Waist circumference (cm)
5. Hip circumference (cm)
6. Inseam length (cm)
7. Shoulder width (cm)

**Item Specifications (5 features):**
1. Brand ID (encoded)
2. Category ID (encoded)
3. Fit type (encoded: 0=slim, 1=regular, 2=loose)
4. Stretch factor (0-1)
5. Size run (-1=runs small, 0=true to size, 1=runs large)

**Feature Scaling:**
StandardScaler applied to all features:
```
X_scaled = (X - mean) / std
```

### Training Methodology

**Dataset Generation:**
- 10,000 synthetic measurement-size pairs
- Based on CDC anthropometric data distributions
- Incorporates brand-specific sizing variations

**Training Split:**
- Training: 7,000 samples (70%)
- Validation: 1,500 samples (15%)
- Test: 1,500 samples (15%)

**Training Process:**
1. Train Random Forest on scaled features
2. Train Neural Network with same data
3. Evaluate both on validation set
4. Determine optimal ensemble weights

**Cross-Validation:**
5-fold stratified cross-validation on training set  
Average CV accuracy: 86.8% ± 1.2%

### Results

| Metric | RF | NN | Ensemble |
|--------|----|----|----------|
| Test Accuracy | 84.2% | 83.6% | 87.4% |
| Within-1-Size Accuracy | 95.1% | 94.8% | 96.8% |
| Mean Absolute Error | 0.18 | 0.19 | 0.15 |

**Size Distribution Performance:**

| Size | Precision | Recall | F1-Score |
|------|-----------|--------|----------|
| XXS | 0.81 | 0.79 | 0.80 |
| XS | 0.85 | 0.83 | 0.84 |
| S | 0.88 | 0.89 | 0.88 |
| M | 0.91 | 0.92 | 0.91 |
| L | 0.89 | 0.88 | 0.88 |
| XL | 0.86 | 0.87 | 0.86 |
| XXL | 0.82 | 0.84 | 0.83 |

### Confidence Calibration

Predictions include confidence scores calibrated using:
```
Calibrated_Confidence = raw_probability ^ (1 / temperature)
```
Optimal temperature: 1.2 (determined via validation)

---

## 3. Style Compatibility Matcher

### Problem Statement
Determine how well multiple clothing items work together as an outfit.

### Architecture

**Model Type:** Siamese Network with Shared Embeddings  
**Base Architecture:** MobileNetV2

**Embedding Network:**
```
Input (224x224x3)
    ↓
MobileNetV2 (frozen)
    ↓
Global Average Pooling
    ↓
Dense (256, ReLU)
    ↓
Dropout (0.3)
    ↓
Dense (128, None)
    ↓
L2 Normalization
    ↓
Output: 128-dim embedding
```

**Compatibility Network:**
```
Item Embeddings [e1, e2, ..., e5]
    ↓
Concatenate
    ↓
Dense (256, ReLU)
    ↓
Dropout (0.4)
    ↓
Dense (128, ReLU)
    ↓
Dropout (0.3)
    ↓
Dense (1, Sigmoid)
    ↓
Output: Compatibility score [0, 1]
```

### Training Methodology

**Dataset Construction:**
- Positive pairs: Professional stylist-curated outfits (3,000 outfits)
- Negative pairs: Random item combinations (3,000 outfits)
- Validation: 600 outfits (300 positive, 300 negative)
- Test: 600 outfits (300 positive, 300 negative)

**Loss Function:**
Binary cross-entropy for compatibility classification

**Training Configuration:**
- Optimizer: Adam (lr=0.001)
- Batch Size: 16 (computationally expensive)
- Epochs: 30
- Data Augmentation: Same as classifier

**Evaluation Protocol:**
1. Model predicts compatibility score
2. Human raters provide binary judgment (compatible/not)
3. Agreement calculated with threshold at 0.5

### Results

| Metric | Value |
|--------|-------|
| Test Accuracy | 84.2% |
| Precision | 0.86 |
| Recall | 0.81 |
| F1-Score | 0.83 |
| AUC-ROC | 0.878 |
| Human Agreement | 82.5% |
| Processing Time | 120ms (3 items) |

**Threshold Analysis:**

| Threshold | Precision | Recall | F1-Score |
|-----------|-----------|--------|----------|
| 0.3 | 0.76 | 0.91 | 0.83 |
| 0.5 | 0.86 | 0.81 | 0.83 |
| 0.7 | 0.92 | 0.68 | 0.78 |

Optimal threshold: 0.5 (balanced precision-recall)

### Similarity Search

Embedding space enables finding similar items:
```
Similarity(i, j) = dot_product(embedding_i, embedding_j)
```

Average retrieval precision@5: 0.78

---

## 4. User Preference Model

### Problem Statement
Generate personalized item recommendations based on user interaction history.

### Architecture

**Hybrid Approach:** Matrix Factorization + Deep Learning

**NMF Component (Collaborative Filtering):**
```
User-Item Matrix (1000 × 500)
    ↓
NMF Decomposition
    ↓
User Factors (1000 × 50)
Item Factors (500 × 50)
```

**Deep Learning Component:**
```
[User_ID (1) + Item_ID (1) + Item_Features (20)]
    ↓
User Embedding (50-dim)
Item Embedding (50-dim)
    ↓
Concatenate with Features
    ↓
Dense (128, ReLU) + Dropout (0.3)
    ↓
Dense (64, ReLU) + Dropout (0.2)
    ↓
Dense (32, ReLU)
    ↓
Dense (1, Sigmoid)
    ↓
Output: Preference score [0, 1]
```

### Training Methodology

**Dataset:**
- 1,000 synthetic users
- 500 items
- 100,000 interactions (10% of possible combinations)
- Interaction types: view (0.3), like (0.7), try-on (0.9), purchase (1.0)

**NMF Training:**
- Algorithm: Coordinate Descent
- Initialization: Random
- Max Iterations: 500
- Regularization: L2 (alpha=0.1)

**Deep Learning Training:**
- Loss: Mean Squared Error
- Optimizer: Adam
- Batch Size: 256
- Epochs: 30

**Cold Start Handling:**
- New users: Use popular items + category preferences
- New items: Use content-based features

### Results

| Metric | NMF Only | DL Only | Hybrid |
|--------|----------|---------|--------|
| Precision@10 | 0.31 | 0.33 | 0.34 |
| Recall@10 | 0.25 | 0.27 | 0.28 |
| NDCG@10 | 0.38 | 0.40 | 0.41 |
| Coverage | 72% | 81% | 78% |

**User Study Results:**
- Relevance Rating: 4.1/5.0
- Diversity Score: 0.65
- Serendipity Score: 0.58

---

## Model Deployment

### Inference Optimization

**Fashion Classifier:**
- Batch inference for multiple items
- Model quantization (FP32 → INT8): 3.2x speedup
- TensorRT optimization: 4.5x speedup
- Final inference: 10ms per image (optimized)

**Size Recommender:**
- Lightweight model (< 5MB)
- CPU-friendly (no GPU required)
- Average inference: 2ms

**Style Matcher:**
- Pre-compute item embeddings
- Store in vector database
- Real-time compatibility: 120ms → 5ms (cached)

**User Preference:**
- Pre-compute user factors during login
- Batch item scoring
- Top-K recommendations: 50ms for 500 items

### Model Versioning

Models tracked with metadata:
- Version number (semantic versioning)
- Training date and duration
- Dataset size and composition
- Performance metrics
- Model file hash

Example:
```json
{
  "model_name": "fashion_classifier",
  "version": "1.2.0",
  "training_date": "2024-11-01",
  "accuracy": 0.923,
  "file_hash": "sha256:abc123..."
}
```

### Continuous Learning

**Feedback Loop:**
1. Collect user feedback (ratings, corrections)
2. Accumulate until threshold (1000 samples)
3. Retrain model with combined data
4. Evaluate on holdout set
5. Deploy if improvement > 1%

**A/B Testing:**
- Champion-Challenger approach
- 90% traffic to current model
- 10% traffic to new model
- Compare metrics over 1 week
- Promote if statistically significant improvement

---

## Ethical Considerations

### Bias Mitigation

**Data Diversity:**
- Ensure representation across sizes (XXS to XXL)
- Include diverse body types in training data
- Balance gender representation
- Cultural sensitivity in style categorization

**Fairness Metrics:**
- Equal accuracy across demographic groups
- Disparate impact ratio > 0.8
- Regular bias audits

### Privacy

- No personally identifiable information in training
- Synthetic user interaction data
- Anonymized user measurements
- GDPR-compliant data handling

### Transparency

- Confidence scores provided with predictions
- Explanation generation for recommendations
- Model card documentation
- Open methodology

---

## Future Improvements

### Short-term (3-6 months)

1. **Multi-modal Learning**
   - Combine visual + textual features
   - Product descriptions in recommendations

2. **Active Learning**
   - Identify uncertain predictions
   - Request human labeling
   - Improve model incrementally

3. **Personalized Embeddings**
   - User-specific style embeddings
   - Adapt to individual preferences

### Long-term (6-12 months)

1. **3D Body Reconstruction**
   - SMPL model integration
   - More accurate measurements
   - Better fit prediction

2. **Temporal Modeling**
   - Capture fashion trends over time
   - Seasonal recommendations
   - Style evolution tracking

3. **Multi-task Learning**
   - Joint training across tasks
   - Shared representations
   - Improved efficiency

---

## References

1. He, K., et al. (2016). "Deep Residual Learning for Image Recognition." CVPR.
2. Breiman, L. (2001). "Random Forests." Machine Learning, 45(1), 5-32.
3. Sandler, M., et al. (2018). "MobileNetV2: Inverted Residuals and Linear Bottlenecks." CVPR.
4. Lee, D.D. & Seung, H.S. (1999). "Learning the parts of objects by non-negative matrix factorization." Nature.
5. McAuley, J., et al. (2015). "Image-based Recommendations on Styles and Substitutes." SIGIR.
