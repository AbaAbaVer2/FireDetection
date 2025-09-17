import json
import base64
import io
from PIL import Image
import numpy as np
import traceback

# 把前端传来的图片数据转换成二进制编码
def get_image_byte(request):
    try:
        # 尝试从请求体获取数据
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            print("JSON解析错误:", e)
            print("接收到的数据:", request.body)
            raise ValueError(f"JSON解析错误: {e}")
            
        if 'image' not in data:
            print("缺少image字段")
            print("接收到的数据字段:", data.keys())
            raise ValueError("请求中缺少image字段")
            
        image_data = data['image']
        # 解码图像数据
        try:
            # 检查是否有逗号分隔符（Data URL格式）
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            # 获取图片的二进制编码
            image_bytes = base64.b64decode(image_data)
            print("图像解码成功，大小:", len(image_bytes), "字节")
            return image_bytes
        except Exception as e:
            print("Base64解码错误:", e)
            raise ValueError(f"Base64解码错误: {e}")
    except Exception as e:
        print("图像二进制获取失败:", e)
        print(traceback.format_exc())
        raise

# 把前端传来的图片数据转换成图片矩阵数据
def get_image_array(request):
    try:
        # 获取二进制数据
        image_bytes = get_image_byte(request)
        
        # 将二进制数据转换为图片
        try:
            img = Image.open(io.BytesIO(image_bytes))
            print("图片打开成功，尺寸:", img.size)
            
            # 转换成图片矩阵
            img_array = np.array(img)
            print("图片矩阵形状:", img_array.shape)
            return img_array
        except Exception as e:
            print("图像处理错误:", e)
            print(traceback.format_exc())
            raise ValueError(f"图像处理错误: {e}")
    except Exception as e:
        print("图像矩阵转换失败:", e)
        print(traceback.format_exc())
        raise