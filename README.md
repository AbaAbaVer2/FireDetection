# 烟火识别系统

一个基于深度学习的烟火识别与人脸检测系统，可以自动检测图片中的烟火现象，并提供直观的可视化结果。同时带有登陆注册功能

## 功能特点

### 图像检测功能
- ✅ 烟火现象自动识别
- ✅ 标记检测到的烟火区域
- ✅ 支持多个烟火源同时检测
- ✅ 实时显示检测结果
- ✅ 检测结果状态展示

### 人脸识别功能
- ✅ 准确定位人脸位置
- ✅ 提取人脸特征码
- ✅ 计算人脸相似度
- ✅ 支持多张人脸同时检测
- ✅ 人脸位置可视化标记

### 界面设计
- ✅ 简洁直观的操作界面
- ✅ 响应式设计适配多种设备
- ✅ 图片上传区与结果展示区分离
- ✅ 加载动画效果
- ✅ 可重置操作状态

### 用户交互
- ✅ 点击上传图片功能
- ✅ 一键开始检测按钮
- ✅ 检测时间和状态实时显示
- ✅ 重置功能快速清空结果
- ✅ 返回主页选项

## 技术特点

- 使用Django作为后端框架，提供稳定可靠的Web服务
- 集成OpenCV实现高效的图像处理功能
- 采用face_recognition库实现准确的人脸检测和特征提取
- 优化的前端界面设计，提供流畅的用户体验
- 使用异步请求处理图像上传和检测流程
- RESTful API设计，便于系统扩展
- 高效的图像处理算法，确保检测精度

## 截图
<img width="1431" height="880" alt="D{BZ YT~)R%4~_MA0BV_KCC" src="https://github.com/user-attachments/assets/7b914520-66ef-4af1-a0b4-1c3a592d44d2" />
<img width="1418" height="959" alt="M2T4TKW(A$`@~6XX@$E(KEF" src="https://github.com/user-attachments/assets/761498cc-c87c-4892-9062-64c51b06b912" />

<img width="1576" height="1121" alt="6V%(S(4 I7NQQ~3 SF Q8JV" src="https://github.com/user-attachments/assets/460b9143-00ca-4dcb-9c7f-13ad646486ca" />
<img width="1832" height="1325" alt="KB(~CA })HDINU6`%7WRL" src="https://github.com/user-attachments/assets/9d5f392b-8241-4103-844f-d76abbc83639" />


## 开发环境

- Python 3.7+
- Django 最新版
- OpenCV 4.x
- face_recognition
- NumPy
- 支持现代浏览器（Chrome、Firefox、Edge等）

## 如何使用

1. 克隆仓库：
   ```bash
   git clone https://github.com/yourusername/fire-detection-system.git
   ```

2. 创建并激活虚拟环境：
   ```bash
   conda create -n fire-detection python=3.8
   conda activate fire-detection
   ```

3. 安装依赖：
   ```bash
   pip install django opencv-python face_recognition numpy
   ```

4. 运行服务器：
   ```bash
   python manage.py runserver
   ```

5. 访问系统：
   ```
   http://127.0.0.1:8000/static/index.html
   ```

## 使用流程

1. 打开系统主页
2. 点击左侧上传区域选择图片（支持JPG、PNG格式）
3. 点击"开始检测"按钮
4. 等待系统处理（右侧会显示加载动画）
5. 查看右侧的检测结果图像和下方的检测信息
6. 可点击"重置"按钮清空当前结果

## 项目结构
```
fire-detection-system/
│
├── controller/            # 控制器模块
├── face_recognite/        # Django应用程序
│   ├── settings.py        # 项目设置
│   ├── urls.py            # URL路由配置
│   └── wsgi.py            # WSGI配置
├── static/                # 静态资源
│   ├── index.html         # 主页
│   └── detection_detect.html  # 检测页面
├── util/                  # 工具函数
├── manage.py              # Django管理脚本
└── README.md              # 项目说明
```

## 鸣谢

- 感谢Django框架提供的Web开发支持
- 感谢OpenCV和face_recognition提供的强大图像处理能力
- 图标和设计元素来源：开源图标库

