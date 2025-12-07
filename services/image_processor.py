"""
图像处理服务
提取人脸特征用于后续分析
"""

import cv2
import numpy as np
from PIL import Image
import os

class ImageProcessor:
    """图像处理器"""
    
    def __init__(self):
        """初始化处理器"""
        # 加载人脸检测模型
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.dcml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
    
    def extract_features(self, image_path):
        """
        提取图像特征
        
        Args:
            image_path: 图像路径
            
        Returns:
            dict: 特征字典
        """
        try:
            # 读取图像
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("无法读取图像文件")
            
            # 转换为灰度图
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # 检测人脸
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            if len(faces) == 0:
                # 如果未检测到人脸，使用默认特征
                return self._generate_default_features()
            
            # 使用第一个检测到的人脸
            x, y, w, h = faces[0]
            face_roi = gray[y:y+h, x:x+w]
            
            # 提取特征
            features = self._extract_face_features(face_roi, img)
            
            return features
            
        except Exception as e:
            print(f"图像处理错误: {str(e)}")
            return self._generate_default_features()
    
    def _extract_face_features(self, face_roi, original_img):
        """提取人脸特征"""
        # 计算面部比例
        h, w = face_roi.shape
        face_ratio = w / h if h > 0 else 1.0
        
        # 计算亮度
        brightness = np.mean(face_roi)
        
        # 计算对比度
        contrast = np.std(face_roi)
        
        # 纹理复杂度
        laplacian = cv2.Laplacian(face_roi, cv2.CV_64F)
        texture = np.var(laplacian)
        
        # 对称性
        left_half = face_roi[:, :w//2]
        right_half = cv2.flip(face_roi[:, w//2:], 1)
        min_width = min(left_half.shape[1], right_half.shape[1])
        symmetry = np.corrcoef(
            left_half[:, :min_width].flatten(),
            right_half[:, :min_width].flatten()
        )[0, 1]
        
        # 边缘密度
        edges = cv2.Canny(face_roi, 100, 200)
        edge_density = np.sum(edges > 0) / (h * w)
        
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
        """生成默认特征（未检测到人脸时使用）"""
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