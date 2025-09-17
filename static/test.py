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
        if len(results)==0 or len(results[0].boxes)==0:
            print("error1234567890-098765432!")
            return  JsonResponse({"code":500,"msg":"没有检测到目标"})

        # 保存处理后的结果
        result_img_array=results[0].plot()
        cv.imwrite(result_path,result_img_array)

        # 构造url返回给前端
        result_url=f"/static/images/{result_name}"
        return JsonResponse({"code":200,"msg":"返回成功","processed_img_url":result_url})
