"""Generate comprehensive fashion dataset"""
import json
import random
import os

# Base data for generation
brands = {
    "shirts": ["Gap", "Ralph Lauren", "Uniqlo", "J.Crew", "Banana Republic", "Zara", "H&M", "Brooks Brothers"],
    "pants": ["Levi's", "Wrangler", "Dockers", "Nike", "Zara", "Gap", "Carhartt", "Lululemon"],
    "dresses": ["Free People", "Calvin Klein", "DVF", "Reformation", "Kate Spade", "Anthropologie", "Zara", "Mango"],
    "jackets": ["AllSaints", "J.Crew", "Alpha Industries", "The North Face", "Levi's", "Barbour", "Patagonia"],
    "shoes": ["Nike", "Adidas", "Converse", "Dr. Martens", "Timberland", "Cole Haan", "Birkenstock"],
    "accessories": ["Kate Spade", "Coach", "Michael Kors", "Tory Burch", "Fossil", "Ray-Ban", "Pandora"]
}

colors = ["black", "white", "gray", "navy", "blue", "red", "green", "brown", "beige", "pink", "purple", "yellow"]
style_tags = {
    "shirts": ["casual", "formal", "business-casual", "sporty", "vintage", "minimalist"],
    "pants": ["casual", "formal", "athletic", "business-casual", "trendy", "classic"],
    "dresses": ["casual", "formal", "cocktail", "summer", "elegant", "romantic"],
    "jackets": ["casual", "formal", "sporty", "outdoor", "classic", "trendy"],
    "shoes": ["casual", "formal", "athletic", "comfortable", "trendy"],
    "accessories": ["casual", "formal", "trendy", "vintage", "minimalist"]
}

# Get the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(script_dir, '..', 'data', 'datasets', 'fashion_items_200.json')

# Load existing items (first 50)
with open(dataset_path, 'r') as f:
    items = json.load(f)

next_id = 51

# Generate shirts (30 more = 40 total)
shirt_names = [
    "Striped Dress Shirt", "Graphic Tee", "Turtleneck Sweater", "Denim Shirt",
    "Athletic Tank Top", "Plaid Flannel", "Hoodie Pullover", "Zip-Up Hoodie",
    "Band Tee", "Long Sleeve Henley", "Mock Neck Top", "Quarter Zip Pullover",
    "Rugby Shirt", "Baseball Tee", "Thermal Long Sleeve", "Crewneck Sweatshirt",
    "Muscle Tee", "Hawaiian Shirt", "Chambray Shirt", "Performance Polo",
    "Cashmere Sweater", "Shawl Cardigan", "Sleeveless Vest", "Tunic Top",
    "Crop Top", "Off-Shoulder Blouse", "Peasant Top", "Silk Blouse",
    "Cowl Neck Sweater", "Peplum Top"
]

for name in shirt_names:
    price = round(random.uniform(19.99, 149.99), 2)
    color = random.choice(colors)
    brand = random.choice(brands["shirts"])
    tags = random.sample(style_tags["shirts"], min(3, len(style_tags["shirts"])))
    
    item = {
        "id": next_id,
        "name": name,
        "description": f"High-quality {name.lower()} perfect for any occasion",
        "category": "shirts",
        "brand": brand,
        "price": price,
        "image_url": f"https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&sig={next_id}",
        "sizes_available": ["XS", "S", "M", "L", "XL"],
        "ar_compatible": True,
        "style_tags": tags,
        "colors": [color],
        "size_chart": {"S": {"chest": 36, "length": 28}, "M": {"chest": 40, "length": 29}, "L": {"chest": 44, "length": 30}}
    }
    items.append(item)
    next_id += 1

# Generate pants (30 more = 40 total)
pant_names = [
    "Straight Leg Jeans", "Athletic Track Pants", "Corduroy Pants", "Linen Pants",
    "Palazzo Pants", "Culottes", "Capri Pants", "Sweatpants", "Yoga Pants",
    "Leather Pants", "Pleated Trousers", "Cropped Pants", "Harem Pants",
    "Jumpsuit", "Overalls", "Paperbag Pants", "Cigarette Pants", "Tapered Pants",
    "Flare Jeans", "Mom Jeans", "Boyfriend Jeans", "Jeggings", "Ponte Pants",
    "Tuxedo Pants", "Drawstring Pants", "Bermuda Shorts", "Athletic Shorts",
    "Tailored Shorts", "Bike Shorts", "Board Shorts"
]

for name in pant_names:
    price = round(random.uniform(29.99, 179.99), 2)
    color = random.choice(colors)
    brand = random.choice(brands["pants"])
    tags = random.sample(style_tags["pants"], min(3, len(style_tags["pants"])))
    
    sizes = ["28", "30", "32", "34", "36"] if "Jeans" in name or "Shorts" in name else ["XS", "S", "M", "L", "XL"]
    
    item = {
        "id": next_id,
        "name": name,
        "description": f"Comfortable {name.lower()} with modern styling",
        "category": "pants",
        "brand": brand,
        "price": price,
        "image_url": f"https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&sig={next_id}",
        "sizes_available": sizes,
        "ar_compatible": True,
        "style_tags": tags,
        "colors": [color],
        "size_chart": {"30": {"waist": 30, "inseam": 32}, "32": {"waist": 32, "inseam": 32}, "34": {"waist": 34, "inseam": 32}}
    }
    items.append(item)
    next_id += 1

# Generate dresses (30 more = 40 total)
dress_names = [
    "A-Line Dress", "Bodycon Dress", "Shift Dress", "Sheath Dress",
    "Slip Dress", "Tunic Dress", "Sweater Dress", "Shirt Dress",
    "Pinafore Dress", "Babydoll Dress", "Asymmetric Dress", "High-Low Dress",
    "Mermaid Dress", "Ball Gown", "Empire Waist Dress", "Halter Dress",
    "Strapless Dress", "One-Shoulder Dress", "Cap Sleeve Dress", "Puff Sleeve Dress",
    "Smocked Dress", "Tiered Dress", "Ruffled Dress", "Pleated Dress",
    "Sequin Dress", "Velvet Dress", "Satin Dress", "Chiffon Dress",
    "Jersey Dress", "Knit Dress"
]

for name in dress_names:
    price = round(random.uniform(49.99, 298.00), 2)
    color = random.choice(colors)
    brand = random.choice(brands["dresses"])
    tags = random.sample(style_tags["dresses"], min(3, len(style_tags["dresses"])))
    
    item = {
        "id": next_id,
        "name": name,
        "description": f"Beautiful {name.lower()} for special occasions",
        "category": "dresses",
        "brand": brand,
        "price": price,
        "image_url": f"https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&sig={next_id}",
        "sizes_available": ["XS", "S", "M", "L"],
        "ar_compatible": True,
        "style_tags": tags,
        "colors": [color],
        "size_chart": {"S": {"bust": 34, "waist": 27, "length": 36}, "M": {"bust": 36, "waist": 29, "length": 37}}
    }
    items.append(item)
    next_id += 1

# Generate jackets (30 more = 40 total)
jacket_names = [
    "Varsity Jacket", "Harrington Jacket", "Coach Jacket", "Anorak",
    "Quilted Jacket", "Shearling Jacket", "Suede Jacket", "Corduroy Jacket",
    "Fleece Jacket", "Softshell Jacket", "Rain Jacket", "Parka",
    "Duffle Coat", "Car Coat", "Barn Jacket", "Work Jacket",
    "Track Jacket", "Kimono Jacket", "Cape Coat", "Poncho",
    "Blazer Jacket", "Sports Coat", "Dinner Jacket", "Cardigan Coat",
    "Teddy Bear Jacket", "Sherpa Jacket", "Utility Jacket", "Safari Jacket",
    "Moto Jacket", "Aviator Jacket"
]

for name in jacket_names:
    price = round(random.uniform(79.99, 595.00), 2)
    color = random.choice(colors)
    brand = random.choice(brands["jackets"])
    tags = random.sample(style_tags["jackets"], min(3, len(style_tags["jackets"])))
    
    item = {
        "id": next_id,
        "name": name,
        "description": f"Stylish {name.lower()} for all seasons",
        "category": "jackets",
        "brand": brand,
        "price": price,
        "image_url": f"https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&sig={next_id}",
        "sizes_available": ["XS", "S", "M", "L", "XL"],
        "ar_compatible": True,
        "style_tags": tags,
        "colors": [color],
        "size_chart": {"S": {"chest": 38, "length": 26, "sleeve": 24}, "M": {"chest": 41, "length": 27, "sleeve": 25}}
    }
    items.append(item)
    next_id += 1

# Generate shoes (30 more = 40 total)
shoe_names = [
    "Slip-On Sneakers", "Low-Top Sneakers", "Platform Sneakers", "Chunky Sneakers",
    "Retro Runners", "Trail Runners", "Cross Trainers", "Training Shoes",
    "Walking Shoes", "Boat Shoes", "Driving Shoes", "Espadrilles",
    "Monk Strap Shoes", "Brogues", "Derby Shoes", "Dress Loafers",
    "Ballet Flats", "Mary Janes", "Pumps", "Stilettos",
    "Wedges", "Ankle Boots", "Knee-High Boots", "Over-the-Knee Boots",
    "Combat Boots", "Work Boots", "Cowboy Boots", "Rain Boots",
    "Flip-Flops", "Slides"
]

for name in shoe_names:
    price = round(random.uniform(49.99, 395.00), 2)
    color = random.choice(colors)
    brand = random.choice(brands["shoes"])
    tags = random.sample(style_tags["shoes"], min(3, len(style_tags["shoes"])))
    
    item = {
        "id": next_id,
        "name": name,
        "description": f"Quality {name.lower()} for everyday comfort",
        "category": "shoes",
        "brand": brand,
        "price": price,
        "image_url": f"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&sig={next_id}",
        "sizes_available": ["7", "8", "9", "10", "11"],
        "ar_compatible": False,
        "style_tags": tags,
        "colors": [color],
        "size_chart": {"8": {"length": 26.0}, "9": {"length": 26.5}, "10": {"length": 27.0}}
    }
    items.append(item)
    next_id += 1

# Generate accessories (40 items)
accessory_items = [
    ("Leather Tote Bag", 120.00), ("Crossbody Bag", 85.00),
    ("Backpack", 98.00), ("Clutch Purse", 65.00),
    ("Messenger Bag", 110.00), ("Weekender Bag", 145.00),
    ("Belt Bag", 45.00), ("Shoulder Bag", 95.00),
    ("Satchel", 135.00), ("Hobo Bag", 125.00),
    ("Aviator Sunglasses", 150.00), ("Wayfarer Sunglasses", 145.00),
    ("Cat Eye Sunglasses", 120.00), ("Round Sunglasses", 135.00),
    ("Leather Belt", 45.00), ("Canvas Belt", 25.00),
    ("Woven Belt", 35.00), ("Chain Belt", 55.00),
    ("Silk Scarf", 75.00), ("Wool Scarf", 65.00),
    ("Cotton Scarf", 35.00), ("Infinity Scarf", 40.00),
    ("Leather Wallet", 85.00), ("Card Holder", 45.00),
    ("Zip Wallet", 95.00), ("Bifold Wallet", 65.00),
    ("Baseball Cap", 30.00), ("Beanie", 25.00),
    ("Fedora", 60.00), ("Bucket Hat", 35.00),
    ("Wide Brim Hat", 55.00), ("Panama Hat", 75.00),
    ("Analog Watch", 195.00), ("Digital Watch", 125.00),
    ("Smart Watch", 299.00), ("Chronograph Watch", 425.00),
    ("Stud Earrings", 45.00), ("Hoop Earrings", 55.00),
    ("Pendant Necklace", 85.00), ("Charm Bracelet", 95.00)
]

for name, price in accessory_items:
    color = random.choice(colors)
    brand = random.choice(brands["accessories"])
    tags = random.sample(style_tags["accessories"], min(2, len(style_tags["accessories"])))
    
    item = {
        "id": next_id,
        "name": name,
        "description": f"Stylish {name.lower()} to complete your outfit",
        "category": "accessories",
        "brand": brand,
        "price": price,
        "image_url": f"https://images.unsplash.com/photo-1523779105320-d1cd346ff52b?w=400&sig={next_id}",
        "sizes_available": ["One Size"],
        "ar_compatible": False,
        "style_tags": tags,
        "colors": [color],
        "size_chart": {}
    }
    items.append(item)
    next_id += 1

# Save the complete dataset
output_path = os.path.join(script_dir, '..', 'data', 'datasets', 'fashion_items.json')
with open(output_path, 'w') as f:
    json.dump(items, f, indent=2)

print(f"Generated {len(items)} fashion items")
print(f"Categories distribution:")
categories = {}
for item in items:
    cat = item['category']
    categories[cat] = categories.get(cat, 0) + 1
for cat, count in sorted(categories.items()):
    print(f"  {cat}: {count}")
