#!/usr/bin/env python3
"""命运预测系统 - Logo/Favicon 生成器"""

from PIL import Image, ImageDraw
import os
import math

def create_gradient_background(size):
    """创建渐变背景"""
    img = Image.new('RGB', (size, size))
    draw = ImageDraw.Draw(img)
    for y in range(size):
        ratio = y / size
        r = int(102 + (118 - 102) * ratio)
        g = int(126 + (75 - 126) * ratio)
        b = int(234 + (162 - 234) * ratio)
        draw.rectangle([(0, y), (size, y+1)], fill=(r, g, b))
    return img

def draw_star(draw, center_x, center_y, radius, fill='white'):
    """绘制星星"""
    points = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        r = radius if i % 2 == 0 else radius * 0.4
        x = center_x + r * math.cos(angle)
        y = center_y - r * math.sin(angle)
        points.append((x, y))
    draw.polygon(points, fill=fill)

def create_logo(size=512):
    """创建logo"""
    img = create_gradient_background(size)
    draw = ImageDraw.Draw(img)
    center = size // 2
    scale = size / 512
    
    # 主圆形
    circle_radius = int(150 * scale)
    main_bbox = [center - circle_radius, center - circle_radius,
                 center + circle_radius, center + circle_radius]
    draw.ellipse(main_bbox, fill=(139, 92, 246), outline=(109, 40, 217), width=int(3 * scale))
    
    # 内圈
    inner_radius = int(130 * scale)
    inner_bbox = [center - inner_radius, center - inner_radius,
                  center + inner_radius, center + inner_radius]
    draw.ellipse(inner_bbox, outline=(200, 180, 255), width=int(2 * scale))
    
    # 中心大星星
    draw_star(draw, center, center, int(60 * scale), fill='white')
    
    # 周围小星星
    for i in range(6):
        angle = i * math.pi / 3
        distance = int(90 * scale)
        x = center + distance * math.cos(angle)
        y = center + distance * math.sin(angle)
        star_size = int((15 + i % 3 * 3) * scale)
        draw_star(draw, x, y, star_size, fill='white')
    
    return img

def generate_favicon_files():
    """生成所有favicon文件"""
    print("正在生成 Logo 和 Favicon...")
    os.makedirs('static', exist_ok=True)
    
    # 生成不同尺寸
    sizes = {
        512: 'static/logo-512.png',
        256: 'static/logo-256.png',
        64: 'static/favicon-64.png',
        32: 'static/favicon-32.png',
        16: 'static/favicon-16.png'
    }
    
    for size, filename in sizes.items():
        img = create_logo(size)
        img.save(filename, 'PNG')
        print(f"✓ 创建: {filename}")
    
    # 创建 .ico 文件
    print("\n正在创建 favicon.ico...")
    logo_16 = create_logo(16)
    logo_32 = create_logo(32)
    logo_48 = create_logo(48)
    
    logo_16.save('static/favicon.ico', format='ICO', 
                 sizes=[(16, 16), (32, 32), (48, 48)])
    print("✓ 创建: static/favicon.ico")
    
    # Apple Touch Icon
    logo_180 = create_logo(180)
    logo_180.save('static/apple-touch-icon.png', 'PNG')
    print("✓ 创建: static/apple-touch-icon.png")
    
    print("\n" + "="*50)
    print("所有文件生成完成！")
    print("="*50)

if __name__ == '__main__':
    try:
        generate_favicon_files()
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
