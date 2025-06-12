import colorsys
from collections import namedtuple

ColorCombination = namedtuple('ColorCombination', ['name', 'colors'])

COLOR_DB = {
    # Luxury color palette
    "Ivory": "#FFFFF0", "Cashmere": "#E6D5B8", "Pearl": "#F0F0F0",
    "Onyx": "#353839", "Gold": "#FFD700", "Platinum": "#E5E4E2",
    "Burgundy": "#800020", "Navy": "#000080", "Emerald": "#50C878",
    "Sapphire": "#082567", "Ruby": "#E0115F", "Amethyst": "#9966CC"
}

def hex_to_hsl(hex_color):
    """Convert hex to HSL color space"""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h, s, l

def generate_luxury_recommendations(hex_color):
    """Generate luxury outfit combinations"""
    h, s, l = hex_to_hsl(hex_color)
    
    brightness = "light" if l > 0.7 else "medium" if l > 0.4 else "dark"
    undertone = "warm" if h < 0.1 or h > 0.9 else "cool" if h > 0.55 and h < 0.7 else "neutral"
    
    # Luxury combinations
    combinations = []
    
    # 1. Classic Luxury
    classic = ["Ivory", "Onyx", "Gold"]
    combinations.append(ColorCombination("Classic Luxury", classic))
    
    # 2. Modern Contrast
    contrast = ["Pearl", "Burgundy", "Platinum"]
    combinations.append(ColorCombination("Modern Contrast", contrast))
    
    # 3. Jewel Tones
    jewels = ["Emerald", "Sapphire", "Ruby", "Amethyst"]
    combinations.append(ColorCombination("Jewel Tones", jewels))
    
    # 4. Seasonal Collection
    seasonal = {
        "warm": ["Cashmere", "Gold", "Burgundy"],
        "cool": ["Pearl", "Platinum", "Navy"],
        "neutral": ["Ivory", "Onyx", "Emerald"]
    }
    combinations.append(ColorCombination(f"{undertone.capitalize()} Elegance", seasonal[undertone]))
    
    return combinations, brightness, undertone

# generated_val = generate_luxury_recommendations("#c1ba9a")
# print(generated_val)