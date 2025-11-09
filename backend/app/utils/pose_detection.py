"""MediaPipe pose detection integration"""
import mediapipe as mp
import numpy as np
import cv2
from typing import Dict, List, Tuple, Optional


class PoseDetector:
    """Pose detection using MediaPipe"""
    
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5
        )
    
    def detect_pose(self, image: np.ndarray) -> Optional[Dict]:
        """Detect pose landmarks in image"""
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process image
        results = self.pose.process(image_rgb)
        
        if not results.pose_landmarks:
            return None
        
        # Extract landmarks
        landmarks = []
        for landmark in results.pose_landmarks.landmark:
            landmarks.append({
                "x": landmark.x,
                "y": landmark.y,
                "z": landmark.z,
                "visibility": landmark.visibility
            })
        
        return {
            "landmarks": landmarks,
            "segmentation_mask": results.segmentation_mask
        }
    
    def extract_body_measurements(self, landmarks: List[Dict], image_shape: Tuple) -> Dict:
        """Extract body measurements from landmarks"""
        h, w = image_shape[:2]
        
        # Key landmark indices
        LEFT_SHOULDER = 11
        RIGHT_SHOULDER = 12
        LEFT_HIP = 23
        RIGHT_HIP = 24
        LEFT_KNEE = 25
        RIGHT_KNEE = 26
        LEFT_ANKLE = 27
        RIGHT_ANKLE = 28
        
        def distance(p1_idx: int, p2_idx: int) -> float:
            p1 = landmarks[p1_idx]
            p2 = landmarks[p2_idx]
            dx = (p1["x"] - p2["x"]) * w
            dy = (p1["y"] - p2["y"]) * h
            return np.sqrt(dx**2 + dy**2)
        
        measurements = {
            "shoulder_width": distance(LEFT_SHOULDER, RIGHT_SHOULDER),
            "torso_length": (distance(LEFT_SHOULDER, LEFT_HIP) + distance(RIGHT_SHOULDER, RIGHT_HIP)) / 2,
            "hip_width": distance(LEFT_HIP, RIGHT_HIP),
            "leg_length": (distance(LEFT_HIP, LEFT_ANKLE) + distance(RIGHT_HIP, RIGHT_ANKLE)) / 2,
            "upper_leg_length": (distance(LEFT_HIP, LEFT_KNEE) + distance(RIGHT_HIP, RIGHT_KNEE)) / 2,
            "lower_leg_length": (distance(LEFT_KNEE, LEFT_ANKLE) + distance(RIGHT_KNEE, RIGHT_ANKLE)) / 2
        }
        
        return measurements
    
    def get_pose_quality_score(self, landmarks: List[Dict]) -> float:
        """Calculate pose quality score (0-100)"""
        # Check visibility of key landmarks
        key_landmarks = [11, 12, 23, 24, 25, 26, 27, 28]  # shoulders, hips, knees, ankles
        
        visibilities = [landmarks[idx]["visibility"] for idx in key_landmarks]
        avg_visibility = sum(visibilities) / len(visibilities)
        
        # Check if person is facing camera (symmetry)
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]
        symmetry = 1.0 - abs(left_shoulder["z"] - right_shoulder["z"])
        
        # Combined score
        quality_score = (avg_visibility * 0.7 + symmetry * 0.3) * 100
        
        return quality_score
    
    def draw_pose(self, image: np.ndarray, landmarks: List[Dict]) -> np.ndarray:
        """Draw pose landmarks on image"""
        # Convert landmarks back to MediaPipe format
        mp_landmarks = self.mp_pose.PoseLandmark
        
        # Create a copy of the image
        annotated_image = image.copy()
        
        # Draw landmarks
        # Note: This is a simplified version
        h, w = image.shape[:2]
        for idx, landmark in enumerate(landmarks):
            x = int(landmark["x"] * w)
            y = int(landmark["y"] * h)
            cv2.circle(annotated_image, (x, y), 5, (0, 255, 0), -1)
        
        return annotated_image
    
    def close(self):
        """Clean up resources"""
        self.pose.close()


def analyze_fit_from_pose(
    user_measurements: Dict,
    item_measurements: Dict,
    tolerance: float = 0.1
) -> Dict:
    """Analyze fit based on measurements"""
    fit_analysis = {
        "overall_fit": "perfect",
        "fit_score": 100.0,
        "details": {},
        "recommendations": []
    }
    
    # Compare measurements
    for key in user_measurements:
        if key in item_measurements:
            user_val = user_measurements[key]
            item_val = item_measurements[key]
            
            diff_ratio = abs(user_val - item_val) / item_val
            
            if diff_ratio < tolerance:
                fit_analysis["details"][key] = "perfect"
            elif diff_ratio < tolerance * 2:
                fit_analysis["details"][key] = "good"
                fit_analysis["fit_score"] -= 5
            else:
                fit_analysis["details"][key] = "poor"
                fit_analysis["fit_score"] -= 15
                
                if user_val > item_val:
                    fit_analysis["recommendations"].append(f"Consider a larger size for better {key}")
                else:
                    fit_analysis["recommendations"].append(f"Consider a smaller size for better {key}")
    
    # Determine overall fit
    if fit_analysis["fit_score"] >= 90:
        fit_analysis["overall_fit"] = "perfect"
    elif fit_analysis["fit_score"] >= 70:
        fit_analysis["overall_fit"] = "good"
    else:
        fit_analysis["overall_fit"] = "needs_adjustment"
    
    return fit_analysis
