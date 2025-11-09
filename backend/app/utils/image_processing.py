"""Image processing utilities"""
import cv2
import numpy as np
from PIL import Image
import base64
import io
from typing import Tuple, Optional


def decode_base64_image(base64_str: str) -> np.ndarray:
    """Decode base64 string to numpy array"""
    # Remove header if present
    if "," in base64_str:
        base64_str = base64_str.split(",")[1]
    
    # Decode
    img_bytes = base64.b64decode(base64_str)
    img = Image.open(io.BytesIO(img_bytes))
    return np.array(img)


def encode_image_to_base64(img: np.ndarray) -> str:
    """Encode numpy array to base64 string"""
    # Convert to PIL Image
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
    
    pil_img = Image.fromarray(img)
    
    # Encode to base64
    buffered = io.BytesIO()
    pil_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"


def resize_image(img: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
    """Resize image to target size"""
    return cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)


def normalize_image(img: np.ndarray) -> np.ndarray:
    """Normalize image to [0, 1] range"""
    return img.astype(np.float32) / 255.0


def preprocess_for_ml(img: np.ndarray, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
    """Preprocess image for ML model input"""
    # Resize
    img = resize_image(img, target_size)
    
    # Normalize
    img = normalize_image(img)
    
    # Add batch dimension
    img = np.expand_dims(img, axis=0)
    
    return img


def apply_clahe(img: np.ndarray) -> np.ndarray:
    """Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)"""
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    
    lab = cv2.merge([l, a, b])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)


def extract_foreground(img: np.ndarray) -> np.ndarray:
    """Extract foreground using GrabCut algorithm"""
    mask = np.zeros(img.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    
    # Define rectangle around the person (approximate)
    h, w = img.shape[:2]
    rect = (int(w * 0.1), int(h * 0.1), int(w * 0.8), int(h * 0.8))
    
    # Apply GrabCut
    cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    
    # Modify mask
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    
    # Apply mask
    result = img * mask2[:, :, np.newaxis]
    
    return result


def detect_skin_tone(img: np.ndarray) -> dict:
    """Detect skin tone from image"""
    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Define skin color range in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    # Create mask
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    # Get mean color
    mean_color = cv2.mean(img, mask=mask)[:3]
    
    return {
        "rgb": [int(c) for c in mean_color],
        "hex": "#{:02x}{:02x}{:02x}".format(int(mean_color[2]), int(mean_color[1]), int(mean_color[0]))
    }
