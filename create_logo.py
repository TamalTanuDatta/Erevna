from PIL import Image, ImageDraw, ImageFont
import os
from math import sin, cos, pi

def create_gradient_circle(draw, center, radius, start_color, end_color, steps=100):
    for i in range(steps):
        ratio = i / steps
        current_radius = radius * (1 - ratio)
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        
        bbox = (
            center[0] - current_radius,
            center[1] - current_radius,
            center[0] + current_radius,
            center[1] + current_radius
        )
        draw.ellipse(bbox, fill=(r, g, b))

def create_orbit_circles(draw, center, radius, num_circles=8):
    for i in range(num_circles):
        angle = 2 * pi * i / num_circles
        x = center[0] + radius * 0.7 * cos(angle)
        y = center[1] + radius * 0.7 * sin(angle)
        
        # Draw small circles in orbit
        circle_radius = radius * 0.12
        circle_bbox = (
            x - circle_radius,
            y - circle_radius,
            x + circle_radius,
            y + circle_radius
        )
        
        # Create a gradient for each orbit circle
        gradient_start = (41, 128, 255)  # Bright blue
        gradient_end = (138, 180, 255)   # Light blue
        for j in range(20):
            ratio = j / 20
            current_radius = circle_radius * (1 - ratio)
            r = int(gradient_start[0] * (1 - ratio) + gradient_end[0] * ratio)
            g = int(gradient_start[1] * (1 - ratio) + gradient_end[1] * ratio)
            b = int(gradient_start[2] * (1 - ratio) + gradient_end[2] * ratio)
            
            current_bbox = (
                x - current_radius,
                y - current_radius,
                x + current_radius,
                y + current_radius
            )
            draw.ellipse(current_bbox, fill=(r, g, b))

def create_logo():
    # Create a new image with a dark background
    width = 800  # Increased width for the full name
    height = 500
    background_color = (20, 24, 35)  # Dark blue-gray
    image = Image.new('RGB', (width, height), background_color)
    
    # Get a drawing context
    draw = ImageDraw.Draw(image)
    
    # Center point
    center = (width//2, height//2)
    
    # Create main circle with gradient
    main_radius = 150
    gradient_start = (0, 82, 204)    # Dark blue
    gradient_end = (41, 128, 255)    # Bright blue
    create_gradient_circle(draw, center, main_radius, gradient_start, gradient_end)
    
    # Add orbiting circles
    create_orbit_circles(draw, center, main_radius)
    
    # Add text
    try:
        # Try to use Arial font if available
        font = ImageFont.truetype("Arial", 120)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    text = "EREVNA"
    text_color = (255, 255, 255)  # White color
    
    # Get text size
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Calculate text position to center it
    text_position = (
        (width - text_width) // 2,
        (height - text_height) // 2
    )
    
    # Draw text with a more pronounced glow effect
    # First draw the outer glow
    glow_colors = [
        (138, 180, 255, 50),  # Light blue with alpha
        (41, 128, 255, 80),   # Medium blue with alpha
        (0, 82, 204, 100)     # Dark blue with alpha
    ]
    
    # Create a temporary image for the glow effect
    glow_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_image)
    
    # Draw multiple layers of glow
    for glow_color in glow_colors:
        for offset in range(8, 0, -1):
            alpha = int(glow_color[3] * (1 - offset/8))
            current_color = (*glow_color[:3], alpha)
            for dx in [-offset, offset]:
                for dy in [-offset, offset]:
                    glow_draw.text(
                        (text_position[0] + dx, text_position[1] + dy),
                        text,
                        font=font,
                        fill=current_color
                    )
    
    # Merge the glow with the main image
    image = Image.alpha_composite(image.convert('RGBA'), glow_image)
    
    # Draw the main text
    draw = ImageDraw.Draw(image)
    draw.text(text_position, text, font=font, fill=text_color)
    
    # Convert back to RGB for saving
    image = image.convert('RGB')
    
    # Save the image
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    image.save(os.path.join(static_dir, 'erevna_logo.png'))

if __name__ == '__main__':
    create_logo()
