import random
import os
import json

# 文件路径，用于保存已生成的随机数
file_path = 'generated_numbers.json'


def load_generated_numbers():
    """从文件中加载已生成的随机数"""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return set(json.load(file))
    return set()



def save_generated_numbers(numbers):
    """将已生成的随机数保存到文件"""
    with open(file_path, 'w') as file:
        json.dump(list(numbers), file)

def generate_unique_random(min_num, max_num):
    """生成一个不重复的随机数"""
    generated_numbers = load_generated_numbers()
    available_numbers = set(range(min_num, max_num + 1)) - generated_numbers

    if not available_numbers:
        raise ValueError("所有可能的数字都已经生成过了。")

    number = random.choice(list(available_numbers))
    generated_numbers.add(number)
    save_generated_numbers(generated_numbers)

    return number

def main():
    min_num = 1
    max_num = 18  # 设定随机数的范围

    try:
        number = generate_unique_random(min_num, max_num)
        print(f"第{number}组开始答辩")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()