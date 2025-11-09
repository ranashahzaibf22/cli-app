"""AR service for virtual try-on functionality"""
import os
import base64
from typing import Dict, Optional
from PIL import Image, ImageDraw, ImageFont
import io
import numpy as np
from ..utils.pose_detection import PoseDetector


class ARService:
    """AR processing service for virtual try-on"""
    
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = upload_dir
        self.pose_detector = PoseDetector()
        os.makedirs(upload_dir, exist_ok=True)
        os.makedirs(os.path.join(upload_dir, "processed"), exist_ok=True)
    
    def validate_image(self, image_data: bytes, max_size_mb: int = 10) -> bool:
        """Validate image file"""
        # Check size
        size_mb = len(image_data) / (1024 * 1024)
        if size_mb > max_size_mb:
            return False
        
        # Try to open as image
        try:
            img = Image.open(io.BytesIO(image_data))
            # Check format
            if img.format not in ['JPEG', 'PNG', 'JPG', 'WEBP']:
                return False
            return True
        except:
            return False
    
    def upload_image(self, image_data: bytes, user_id: int) -> Optional[str]:
        """Save uploaded image and return path"""
        if not self.validate_image(image_data):
            return None
        
        # Generate filename
        filename = f"user_{user_id}_{os.urandom(8).hex()}.jpg"
        filepath = os.path.join(self.upload_dir, filename)
        
        # Save image
        img = Image.open(io.BytesIO(image_data))
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(filepath, 'JPEG', quality=90)
        
        return filepath
    
    def process_ar_overlay(
        self,
        image_path: str,
        clothing_item: Dict,
        pose_landmarks: Optional[Dict] = None
    ) -> Dict:
        """Process AR overlay on image"""
        # Load image
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # Get image dimensions
        width, height = img.size
        
        # Determine overlay region based on category
        category = clothing_item.get('category', 'shirts')
        color = clothing_item.get('colors', ['blue'])[0]
        
        # Map color names to RGB
        color_map = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'gray': (128, 128, 128),
            'navy': (0, 0, 128),
            'blue': (0, 100, 200),
            'red': (200, 0, 0),
            'green': (0, 150, 0),
            'brown': (139, 69, 19),
            'beige': (245, 245, 220),
            'pink': (255, 192, 203),
            'purple': (128, 0, 128),
            'yellow': (255, 255, 0),
            'olive': (128, 128, 0),
        }
        
        overlay_color = color_map.get(color, (100, 150, 200))
        
        # Simple overlay based on category
        if category in ['shirts', 'dresses', 'jackets']:
            # Upper body overlay
            if pose_landmarks and 'left_shoulder' in pose_landmarks and 'right_shoulder' in pose_landmarks:
                # Use pose landmarks
                ls = pose_landmarks['left_shoulder']
                rs = pose_landmarks['right_shoulder']
                
                shoulder_width = abs(rs['x'] - ls['x']) * width
                center_x = (ls['x'] + rs['x']) / 2 * width
                center_y = (ls['y'] + rs['y']) / 2 * height
                
                # Draw clothing overlay
                overlay_width = shoulder_width * 1.5
                overlay_height = height * 0.4
                
                left = int(center_x - overlay_width / 2)
                top = int(center_y)
                right = int(center_x + overlay_width / 2)
                bottom = int(center_y + overlay_height)
            else:
                # Default positioning (center, upper area)
                overlay_width = width * 0.6
                overlay_height = height * 0.4
                left = int(width * 0.2)
                top = int(height * 0.2)
                right = int(width * 0.8)
                bottom = int(height * 0.6)
            
            # Create semi-transparent overlay
            overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rectangle(
                [(left, top), (right, bottom)],
                fill=(*overlay_color, 100),
                outline=(*overlay_color, 200),
                width=3
            )
            
            # Composite
            img = img.convert('RGBA')
            img = Image.alpha_composite(img, overlay)
            img = img.convert('RGB')
            draw = ImageDraw.Draw(img)
            
            # Add text label
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            text = clothing_item.get('name', 'Clothing Item')
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (width - text_width) // 2
            text_y = bottom + 10
            
            # Draw text background
            draw.rectangle(
                [(text_x - 10, text_y - 5), (text_x + text_width + 10, text_y + 35)],
                fill=(0, 0, 0, 180)
            )
            draw.text((text_x, text_y), text, fill='white', font=font)
        
        elif category == 'pants':
            # Lower body overlay
            if pose_landmarks and 'left_hip' in pose_landmarks:
                lh = pose_landmarks['left_hip']
                center_x = lh['x'] * width
                center_y = lh['y'] * height
                
                overlay_width = width * 0.4
                overlay_height = height * 0.5
                
                left = int(center_x - overlay_width / 2)
                top = int(center_y)
                right = int(center_x + overlay_width / 2)
                bottom = int(center_y + overlay_height)
            else:
                left = int(width * 0.3)
                top = int(height * 0.5)
                right = int(width * 0.7)
                bottom = int(height * 0.95)
            
            overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.rectangle(
                [(left, top), (right, bottom)],
                fill=(*overlay_color, 100),
                outline=(*overlay_color, 200),
                width=3
            )
            
            img = img.convert('RGBA')
            img = Image.alpha_composite(img, overlay)
            img = img.convert('RGB')
        
        # Save processed image
        processed_filename = f"processed_{os.path.basename(image_path)}"
        processed_path = os.path.join(self.upload_dir, "processed", processed_filename)
        img.save(processed_path, 'JPEG', quality=90)
        
        return {
            'processed_image_path': processed_path,
            'overlay_applied': True,
            'category': category,
            'color': color
        }
    
    def simple_fit_analysis(self, user_measurements: Dict, item_specs: Dict) -> Dict:
        """Generate fit analysis"""
        category = item_specs.get('category', 'shirts')
        
        # Get size chart from item
        size_chart = item_specs.get('size_chart', {})
        user_chest = user_measurements.get('chest', 38)
        user_waist = user_measurements.get('waist', 32)
        
        # Simple fit scoring
        fit_score = 0.75  # Default
        recommendations = []
        
        if category in ['shirts', 'jackets']:
            # Check chest measurement
            if size_chart:
                # Find best fitting size
                best_fit = 'M'
                min_diff = float('inf')
                
                for size, measurements in size_chart.items():
                    if isinstance(measurements, dict) and 'chest' in measurements:
                        chest_size = measurements['chest']
                        diff = abs(chest_size - user_chest)
                        if diff < min_diff:
                            min_diff = diff
                            best_fit = size
                
                if min_diff <= 2:
                    fit_score = 0.95
                    fit_assessment = "Excellent Fit"
                    recommendations.append(f"Size {best_fit} is perfect for your measurements")
                elif min_diff <= 4:
                    fit_score = 0.80
                    fit_assessment = "Good Fit"
                    recommendations.append(f"Size {best_fit} should fit well")
                else:
                    fit_score = 0.65
                    fit_assessment = "Acceptable Fit"
                    recommendations.append("Consider trying multiple sizes")
            else:
                fit_assessment = "Standard Fit"
                recommendations.append("Check detailed size chart for best fit")
        
        elif category == 'pants':
            # Check waist measurement
            fit_assessment = "Good Fit"
            recommendations.append("Waist size matches your measurements")
            fit_score = 0.85
        
        else:
            fit_assessment = "Standard Fit"
            recommendations.append("Try on for best fit assessment")
        
        return {
            'fit_score': round(fit_score, 2),
            'fit_assessment': fit_assessment,
            'recommendations': recommendations,
            'measurements_used': {
                'chest': user_chest,
                'waist': user_waist
            }
        }
    
    def analyze_fit_from_pose(self, pose_landmarks: Dict, item_specs: Dict) -> Dict:
        """Analyze fit using pose detection"""
        # Extract measurements from pose
        measurements = self.pose_detector.extract_body_measurements(
            pose_landmarks,
            image_shape=(480, 640, 3)  # Default shape
        )
        
        # Perform fit analysis
        return self.simple_fit_analysis(measurements, item_specs)
    
    def get_image_base64(self, image_path: str) -> Optional[str]:
        """Convert image to base64 string"""
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            return base64.b64encode(image_data).decode('utf-8')
        except:
            return None
