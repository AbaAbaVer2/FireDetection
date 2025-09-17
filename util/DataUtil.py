import json
import os

filename='data.json'

def save_json(new_data):
    # 检查文件是否存在
    file_exists = os.path.isfile(filename)

    # 如果文件存在，则读取现有数据；否则初始化为空列表
    if file_exists:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)  # 解析 JSON 数据为 Python 对象
    else:
        data = []  # 初始化为空列表，因为我们假设要存储的是对象列表

    # 向数据列表中添加新数据
    data.append(new_data)

    # 写入更新后的数据到文件
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

#读取数据
def read_json():
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # 加载并解析 JSON 数据
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 不存在。")
        return None
    except json.JSONDecodeError:
        print(f"错误：文件 '{filename}' 不包含有效的 JSON 数据。")
        return None
    except Exception as e:
        print(f"读取文件时发生未知错误: {e}")
        return None
# 获取用户姓名
def get_data_name(num):
    data = read_json()
    #print(data)
    result = [user for user in data if user["num"] == num]
   # print(result)
    return result[0]["name"]

