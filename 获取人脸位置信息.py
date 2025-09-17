import cv2 as cv
import face_recognition

def detect_face_locations(image_path):
    """
    获取图像中的人脸位置信息
    参数:
        image_path: 图像文件路径
    返回:
        人脸位置列表，每个位置是一个元组 (top, right, bottom, left)
    """
    # 读取图像
    img = cv.imread(image_path)
    
    # 获取人脸位置信息
    face_locations = face_recognition.face_locations(img)
    
    # 返回人脸位置列表
    return face_locations

if __name__ == "__main__":
    # 测试代码
    image_path = "./img.jpg"
    locations = detect_face_locations(image_path)
    
    if len(locations) == 0:
        print("未检测到人脸")
    else:
        print(f"检测到 {len(locations)} 个人脸:")
        for i, (top, right, bottom, left) in enumerate(locations):
            print(f"人脸 {i+1}: 上={top}, 右={right}, 下={bottom}, 左={left}")
