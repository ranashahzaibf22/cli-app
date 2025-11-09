"""Groq API integration for AI-powered features"""
from typing import List, Dict, Optional
import os


class GroqService:
    """Groq API service for fashion recommendations and insights"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self.use_groq = bool(self.api_key and self.api_key != "your-groq-api-key-here")
        
        # Try to initialize Groq client if API key is available
        if self.use_groq:
            try:
                from groq import Groq
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"Groq initialization failed: {e}")
                self.use_groq = False
    
    def generate_style_advice(
        self,
        items: List[Dict],
        user_preferences: Dict,
        context: Optional[Dict] = None
    ) -> str:
        """Generate style advice for clothing combinations"""
        item_names = [item.get("name", "item") for item in items]
        categories = [item.get("category", "") for item in items]
        colors = [item.get("colors", [""])[0] if item.get("colors") else "" for item in items]
        
        if self.use_groq:
            try:
                # Create prompt for Groq
                prompt = f"""You are a professional fashion stylist. Provide styling advice for these items:
                
Items: {', '.join(item_names)}
Categories: {', '.join(categories)}
Colors: {', '.join(colors)}
User Preferences: {user_preferences}
Occasion: {context.get('occasion', 'casual') if context else 'casual'}

Provide brief, practical styling advice in 2-3 sentences."""

                response = self.client.chat.completions.create(
                    model="mixtral-8x7b-32768",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=150
                )
                
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"Groq API error: {e}")
                # Fall through to fallback
        
        # Fallback: rule-based advice
        advice = f"These {len(items)} items create a well-coordinated outfit. "
        
        if context and context.get("occasion"):
            occasion = context['occasion']
            if occasion == "formal":
                advice += "The combination is elegant and appropriate for formal occasions. "
            elif occasion == "casual":
                advice += "Perfect for everyday casual wear. "
            elif occasion == "business":
                advice += "Professional and suitable for business settings. "
        
        # Color advice
        unique_colors = list(set(colors))
        if len(unique_colors) <= 2:
            advice += "The color palette is harmonious and easy to coordinate."
        else:
            advice += "Consider limiting to 2-3 main colors for a cohesive look."
        
        return advice
    
    def explain_recommendation(
        self,
        recommended_item: Dict,
        user_history: List[Dict],
        reason: str = "ml_prediction"
    ) -> str:
        """Explain why an item was recommended"""
        item_name = recommended_item.get("name", "this item")
        category = recommended_item.get("category", "")
        price = recommended_item.get("price", 0)
        
        if self.use_groq:
            try:
                prompt = f"""Explain in 1-2 sentences why we're recommending "{item_name}" (a {category} priced at ${price}) 
to a user who has previously shown interest in similar items. Reason: {reason}"""

                response = self.client.chat.completions.create(
                    model="mixtral-8x7b-32768",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.6,
                    max_tokens=100
                )
                
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"Groq API error: {e}")
        
        # Fallback explanation
        if reason == "ml_prediction":
            explanation = f"We recommend {item_name} based on your browsing history and style preferences. "
        elif reason == "trending":
            explanation = f"{item_name} is currently trending and matches your taste. "
        elif reason == "similar":
            explanation = f"{item_name} is similar to items you've previously liked. "
        else:
            explanation = f"{item_name} would be a great addition to your wardrobe. "
        
        explanation += "It complements items you've previously shown interest in."
        
        return explanation
    
    def generate_outfit_ideas(
        self,
        base_item: Dict,
        available_items: List[Dict],
        occasion: Optional[str] = None
    ) -> List[Dict]:
        """Generate complete outfit ideas"""
        # Placeholder implementation
        
        outfits = []
        
        # Simple logic: group items by category
        tops = [i for i in available_items if i.get("category") == "tops"]
        bottoms = [i for i in available_items if i.get("category") == "bottoms"]
        shoes = [i for i in available_items if i.get("category") == "shoes"]
        
        # Create a sample outfit
        if tops and bottoms and shoes:
            outfits.append({
                "items": [tops[0], bottoms[0], shoes[0]],
                "description": "Casual everyday outfit",
                "confidence": 0.85
            })
        
        return outfits[:3]  # Return top 3 outfits
    
    def analyze_color_compatibility(
        self,
        colors: List[str]
    ) -> Dict:
        """Analyze color compatibility"""
        # Placeholder implementation
        
        return {
            "compatible": len(colors) <= 3,  # Simple rule: max 3 colors
            "score": 0.8,
            "advice": "These colors work well together. Consider adding a neutral tone for balance."
        }
