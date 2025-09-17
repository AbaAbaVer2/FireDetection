from django.http import JsonResponse
from util.ImageUtil import  *
import json
import face_recognition
import cv2 as cv
from util.RandomUtil import *
import pymysql
import numpy as np
import sys
import traceback

# 设置控制台输出编码
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

face_url="D:/1STUDY1/Codes/face_recognite/static/face/"
#人脸信息采集
def face_collection(request):
    if request.method == "POST":
        try:
            print("正在接收人脸采集请求...")
            
            # 获取并处理图像
            image_array = get_image_array(request)
            print("图像数组形状:", image_array.shape)
            
            # 把人脸图片转为RGB格式
            try:
                image = cv.cvtColor(image_array, cv.COLOR_BGR2RGB)
                print("颜色转换成功")
            except Exception as e:
                print(f"颜色转换错误: {e}")
                data = {
                    "code": 400,
                    "msg": f"图像处理错误: {e}",
                }
                return JsonResponse(data)
            
            # 获取人脸位置信息
            try:
                face_locations = face_recognition.face_locations(image)
                print(f"检测到 {len(face_locations)} 个人脸")
                
                if len(face_locations) == 0:
                    data = {
                        "code": 400,
                        "msg": "未检测到人脸，请确保面部清晰可见",
                    }
                    return JsonResponse(data)
            except Exception as e:
                print(f"人脸定位错误: {e}")
                data = {
                    "code": 400,
                    "msg": f"人脸检测错误: {e}",
                }
                return JsonResponse(data)
            
            # 检查人脸存储目录是否存在
            if not os.path.exists(face_url):
                os.makedirs(face_url, exist_ok=True)
                print(f"创建人脸存储目录: {face_url}")
                
            # 获取图片二进制码
            image_byte = get_image_byte(request)
            
            # 为图片生成唯一文件名，确保生成在1-1000之间的随机ID
            try:
                name_id = generate_unique_random(1, 1000)
                print(f"生成的ID: {name_id}")
            except ValueError as e:
                # 如果所有ID都被使用，尝试清理并重新开始
                print(f"ID生成错误: {e}")
                # 如果所有ID都被使用，我们可以重置已使用ID列表
                if os.path.exists('generated_numbers.json'):
                    os.remove('generated_numbers.json')
                    print("已重置ID生成器")
                    name_id = generate_unique_random(1, 1000)
                else:
                    data = {
                        "code": 500,
                        "msg": "无法生成唯一ID",
                    }
                    return JsonResponse(data)
            
            # 文件写入人脸图片
            face_file_path = face_url + str(name_id) + ".jpg"
            try:
                with open(face_file_path, "wb") as f:
                    f.write(image_byte)
                print(f"人脸图片已保存至: {face_file_path}")
            except Exception as e:
                print(f"文件写入错误: {e}")
                data = {
                    "code": 500,
                    "msg": f"保存人脸图像失败: {e}",
                }
                return JsonResponse(data)
            
            # 把数据转成字典并获取用户输入的个人信息
            try:
                data = json.loads(request.body.decode('utf-8'))
                name = data['name']
                age = data['age']
                phone = data['phone']
                print(f"用户信息: 姓名={name}, 年龄={age}, 电话={phone}")
            except Exception as e:
                print(f"数据解析错误: {e}")
                data = {
                    "code": 400,
                    "msg": f"数据解析错误: {e}",
                }
                return JsonResponse(data)
            
            # 写入数据库
            result = face_insert(name_id, name, age, phone)
            if result:
                data = {
                    "code": 200,
                    "msg": f"数据写入成功! ID: {name_id}",
                }
            else:
                # 如果数据库写入失败，删除已保存的图片
                if os.path.exists(face_file_path):
                    os.remove(face_file_path)
                    print(f"已删除图片: {face_file_path}")
                
                data = {
                    "code": 400,
                    "msg": "数据写入失败，请检查数据库连接",
                }
            return JsonResponse(data)
        except Exception as e:
            import traceback
            print(f"人脸采集处理错误: {e}")
            print(traceback.format_exc())
            data = {
                "code": 500,
                "msg": f"系统处理错误: {str(e)}",
            }
            return JsonResponse(data)
    else:
        data = {
            "code": 400,
            "msg": "请求方式错误，请使用POST方法",
        }
        return JsonResponse(data)

# 人脸信息验证
def face_detect(request):
    if request.method == "POST":
        try:
            print("正在接收人脸检测请求...")
            image_array = get_image_array(request)
            print(f"图像数组形状: {image_array.shape}")
            
            # 把人脸图片转为RGB格式
            try:
                image = cv.cvtColor(image_array, cv.COLOR_BGR2RGB)
                print("颜色转换成功")
            except Exception as e:
                print(f"颜色转换错误: {e}")
                data = {
                    "code": 400,
                    "msg": f"图像处理错误: {e}",
                }
                return JsonResponse(data)
            
            # 获取人脸位置信息
            try:
                face_locations = face_recognition.face_locations(image)
                print(f"检测到 {len(face_locations)} 个人脸")
                
                if len(face_locations) == 0:
                    data = {
                        "code": 400,
                        "msg": "未检测到人脸",
                    }
                    return JsonResponse(data)
            except Exception as e:
                print(f"人脸定位错误: {e}")
                data = {
                    "code": 400,
                    "msg": f"人脸检测错误: {e}",
                }
                return JsonResponse(data)
                
            # 检查人脸存储目录是否存在
            if not os.path.exists(face_url):
                os.makedirs(face_url, exist_ok=True)
                print(f"创建人脸存储目录: {face_url}")
                
            # 检查是否有任何存储的人脸
            try:
                face_dir = os.listdir(face_url)
                print(f"人脸目录中有 {len(face_dir)} 个文件")
                
                if len(face_dir) == 0:
                    data = {
                        "code": 400,
                        "msg": "没有存储的人脸数据，请先采集人脸",
                    }
                    return JsonResponse(data)
            except Exception as e:
                print(f"读取人脸目录错误: {e}")
                data = {
                    "code": 400,
                    "msg": f"读取人脸数据错误: {e}",
                }
                return JsonResponse(data)
                
            # 获取当前摄像头人脸特征向量
            try:
                image_v = face_recognition.face_encodings(image)[0]
                print("成功提取人脸特征向量")
            except IndexError:
                data = {
                    "code": 400,
                    "msg": "无法提取人脸特征，请保持面部清晰可见",
                }
                return JsonResponse(data)
            except Exception as e:
                print(f"特征提取错误: {e}")
                data = {
                    "code": 400,
                    "msg": f"人脸特征提取错误: {e}",
                }
                return JsonResponse(data)
                
            # 用于存储所有距离数据，方便排序和找出最相似的人脸
            face_distances = []
            
            # 尝试匹配人脸
            for face in face_dir:
                try:
                    # 定义路径
                    face_path = face_url + face
                    print(f"尝试匹配人脸: {face_path}")
                    
                    # 加载存储的人脸图像
                    face_image = face_recognition.load_image_file(face_path)
                    
                    # 获取图像编码
                    face_encodings = face_recognition.face_encodings(face_image)
                    if len(face_encodings) == 0:
                        print(f"无法从存储的图像中提取特征: {face}")
                        continue
                        
                    face_v = face_encodings[0]
                    
                    # 计算相似度（欧氏距离）
                    distance = np.linalg.norm(face_v - image_v)
                    print(f"人脸 {face} 的距离: {distance}")
                    
                    # 提取ID
                    try:
                        face_id = int(face.split(".")[0])
                        face_distances.append((face_id, face, distance))
                    except:
                        print(f"无法解析文件名为ID: {face}")
                        continue
                        
                except Exception as e:
                    print(f"处理存储人脸时出错 {face}: {e}")
                    continue
            
            # 如果没有成功处理的人脸
            if not face_distances:
                data = {
                    "code": 400,
                    "msg": "无法从存储的人脸中提取有效特征",
                }
                return JsonResponse(data)
            
            # 按距离排序（距离越小，相似度越高）
            face_distances.sort(key=lambda x: x[2])
            best_match = face_distances[0]
            best_id, best_face, best_distance = best_match
            
            # 定义相似度阈值（距离小于0.5认为是同一个人）
            threshold = 0.5
            
            if best_distance < threshold:
                # 找到了匹配的人脸，查询详细信息
                try:
                    results = query_info(best_id)
                    
                    if results and len(results) > 0:
                        user_name = results[0][1]  # 用户名在结果的第二列
                        user_age = results[0][2]   # 年龄在结果的第三列
                        user_phone = results[0][3] # 电话在结果的第四列
                        
                        # 返回详细的匹配信息
                        data = {
                            "code": 200,
                            "msg": f"识别成功! ID: {best_id}, 姓名: {user_name}",
                            "match_details": {
                                "id": best_id,
                                "name": user_name,
                                "age": user_age,
                                "phone": user_phone,
                                "similarity": f"{(1-best_distance)*100:.2f}%",
                                "distance": f"{best_distance:.4f}"
                            }
                        }
                    else:
                        data = {
                            "code": 200,
                            "msg": f"识别成功! ID: {best_id}，但未找到详细信息",
                            "match_details": {
                                "id": best_id,
                                "similarity": f"{(1-best_distance)*100:.2f}%",
                                "distance": f"{best_distance:.4f}"
                            }
                        }
                except Exception as e:
                    print(f"获取用户信息错误: {e}")
                    data = {
                        "code": 200,
                        "msg": f"识别到面部 ID: {best_id}，但获取详细信息时出错",
                        "match_details": {
                            "id": best_id,
                            "similarity": f"{(1-best_distance)*100:.2f}%",
                            "distance": f"{best_distance:.4f}"
                        }
                    }
            else:
                # 没有匹配到任何人脸
                # 返回相似度最高的人脸作为参考
                data = {
                    "code": 400,
                    "msg": f"无匹配人脸，最相似的人脸 ID: {best_id}，但相似度不足 (距离: {best_distance:.4f})",
                    "best_match": {
                        "id": best_id,
                        "similarity": f"{(1-best_distance)*100:.2f}%",
                        "distance": f"{best_distance:.4f}"
                    }
                }
            
            return JsonResponse(data)
            
        except Exception as e:
            import traceback
            print(f"人脸检测处理错误: {e}")
            print(traceback.format_exc())
            data = {
                "code": 500,
                "msg": f"系统处理错误: {str(e)}",
            }
            return JsonResponse(data)
    else:
        data = {
            "code": 400,
            "msg": "请求方式错误，请使用POST方法",
        }
        return JsonResponse(data)

# 定义数据库写入操作
def face_insert(id, name, age, phone):
    try:
        # 数据库连接
        conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="your_sql_password",  # 使用更新后的密码
            database="detection",
            charset="utf8mb3"
        )
        print(f"数据库连接成功，准备写入ID: {id}")
        
        # 创建游标对象
        cursor = conn.cursor()
        
        # 创建sql语句
        sql = "insert into user_info(id, user_name, age, phone) values (%s, %s, %s, %s)"
        
        # 执行cursor语句
        cursor.execute(sql, (id, name, age, phone))
        
        # 提交事务
        conn.commit()
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        print(f"数据写入成功，ID: {id}, 姓名: {name}")
        return True
    except Exception as e:
        print(f"数据写入失败: {e}")
        print(traceback.format_exc())
        return False
#定义数据库查询操作
def query_info(id):
    try:
        # 数据库连接
        conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="Disaster04", # 使用更新后的密码
            database="detection",
            charset="utf8mb3"
        )
        print(f"数据库连接成功，准备查询ID: {id}")
        
        # 创建游标对象
        cursor = conn.cursor()
        
        # 创建sql语句
        sql = "select * from user_info where id = %s"
        
        # 执行cursor语句
        cursor.execute(sql, (id,))
        
        # 获取查询结果
        result = cursor.fetchall()
        print(f"查询结果: {result}")
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        return result
    except Exception as e:
        import traceback
        print(f"数据库查询失败: {e}")
        print(traceback.format_exc())
        return None
#目标检测
from ultralytics import YOLO
import uuid
from django.conf import settings
import os

# 检查模型文件是否存在
model_path = "D:/1STUDY1/Codes/face_recognite/controller/best.pt"
if not os.path.exists(model_path):
    print(f"警告: 模型文件 {model_path} 不存在!")
    # 可以添加适当的错误处理
model=YOLO(model_path)
def predict(request):
    if request.method=="POST":
        # 确认上传图片
        if "img" not in request.FILES:
            return JsonResponse({"code":500,"msg":"没有找到图片"},status=400)
        # 获取图片
        image_file=request.FILES["img"]
        print(f"收到的图片名是：{image_file.name}")
        #创建唯一文件名 uuid
        unique_name=f"{uuid.uuid4()}.jpg"
        # 定义上传的图片的存储路径
        img_path=os.path.join(settings.BASE_DIR,"static","images",unique_name)
        print(img_path)
        # 定义检测后的结果图片的路径
        # result_name=f"result_{unique_name}.jpg"
        result_name=f"result_{unique_name}"
        result_path=os.path.join(settings.BASE_DIR,"static","images",result_name)
        print(result_path)
        # 图片写入
        with open(img_path,"wb+") as f:
            for chunk in image_file.chunks():
                f.write(chunk)
        print(f"文件已经写入到了：{img_path}")
        # 使用yolo模型进行预测
        results=model(img_path)
        # 判断是否检测到目标
        #

        # 保存处理后的结果
        result_img_array=results[0].plot()
        cv.imwrite(result_path,result_img_array)

        # 构造url返回给前端
        result_url=f"/static/images/{result_name}"
        return JsonResponse({"code":200,"msg":"返回成功","processed_img_url":result_url})

if __name__ == '__main__':
    query_info(1)