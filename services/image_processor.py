"""
图像处理服务
"""

import cv2
import numpy as np
import os

class ImageProcessor:
    """图像处理器"""
    
    def __init__(self):
        """初始化处理器"""
        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
        except:
            self.face_cascade = None
    
    def extract_features(self, image_path):
        """提取图像特征"""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return self._generate_default_features()
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            if self.face_cascade is not None:
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
                
                if len(faces) > 0:
                    x, y, w, h = faces[0]
                    face_roi = gray[y:y+h, x:x+w]
                    return self._extract_face_features(face_roi, img)
            
            return self._generate_default_features()
            
        except Exception as e:
            print(f"图像处理错误: {e}")
            return self._generate_default_features()
    
    def _extract_face_features(self, face_roi, original_img):
        """提取人脸特征"""
        h, w = face_roi.shape
        face_ratio = w / h if h > 0 else 1.0
        brightness = np.mean(face_roi)
        contrast = np.std(face_roi)
        
        try:
            laplacian = cv2.Laplacian(face_roi, cv2.CV_64F)
            texture = np.var(laplacian)
        except:
            texture = 100.0
        
        try:
            left_half = face_roi[:, :w//2]
            right_half = cv2.flip(face_roi[:, w//2:], 1)
            min_width = min(left_half.shape[1], right_half.shape[1])
            symmetry = np.corrcoef(
                left_half[:, :min_width].flatten(),
                right_half[:, :min_width].flatten()
            )[0, 1]
        except:
            symmetry = 0.8
        
        try:
            edges = cv2.Canny(face_roi, 100, 200)
            edge_density = np.sum(edges > 0) / (h * w)
        except:
            edge_density = 0.15
        
        return {
            'face_ratio': float(face_ratio),
            'brightness': float(brightness),
            'contrast': float(contrast),
            'texture': float(texture),
            'symmetry': float(symmetry),
            'edge_density': float(edge_density),
            'face_width': int(w),
            'face_height': int(h)
        }
    
    def _generate_default_features(self):
        """生成默认特征"""
        return {
            'face_ratio': 0.85,
            'brightness': 127.0,
            'contrast': 50.0,
            'texture': 100.0,
            'symmetry': 0.8,
            'edge_density': 0.15,
            'face_width': 200,
            'face_height': 235
        }
