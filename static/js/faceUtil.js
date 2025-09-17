var faceUtile = {
    width: 500, // 图片宽度
    height: 500, // 图片高度
    isOpen: false, // 是否开启摄像头
    promise: null,
    video: null, // 存储视频元素引用
    canvas: null, // 存储画布元素引用
    
    // 打开摄像头
    openVideo: function(id) {
        var mythis = this;
        try {
            console.log("开始初始化视频元素");
            
            // 清空容器
            $("#" + id).empty();
            
            // 添加视频和画布元素
            let videoComp = 
                "<video id='myVideo' width='" + this.width + "px' height='" + this.height + "px' autoplay='autoplay' style='margin-top: 0px'></video>" +
                "<canvas id='myCavans' width='" + this.width + "px' height='" + this.height + "px' style='display: none'></canvas>";
            
            $("#" + id).append(videoComp);
            
            // 获取视频元素引用
            this.video = document.getElementById("myVideo");
            this.canvas = document.getElementById("myCavans");
            
            // 设置媒体约束条件
            let constraints = {
                video: {
                    width: mythis.width,
                    height: mythis.height,
                    facingMode: 'user' // 使用前置摄像头
                },
                audio: false // 不需要音频
            };
            
            console.log("请求摄像头权限...");
            
            // 请求媒体设备
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                throw new Error("浏览器不支持摄像头API");
            }
            
            this.promise = navigator.mediaDevices.getUserMedia(constraints);
            this.promise.then(function(mediaStream) {
                console.log("摄像头权限获取成功");
                mythis.video.srcObject = mediaStream;
                mythis.video.onloadedmetadata = function() {
                    mythis.video.play();
                    console.log("视频播放开始");
                    mythis.isOpen = true;
                };
            }).catch(function(err) {
                console.error("摄像头访问失败:", err.name, err.message);
                alert("摄像头访问失败: " + err.message);
                mythis.isOpen = false;
            });
        } catch (e) {
            console.error("视频初始化失败:", e);
            alert("视频初始化失败: " + e.message);
            this.isOpen = false;
        }
    },
    
    // 获取图片base64编码
    getDecode: function() {
        try {
            if (!this.isOpen) {
                console.error("摄像头未开启");
                alert("摄像头未开启");
                return null;
            }
            
            if (!this.video || !this.canvas) {
                console.error("视频或画布元素未初始化");
                return null;
            }
            
            console.log("正在捕获图像...");
            let ctx = this.canvas.getContext('2d');
            ctx.drawImage(this.video, 0, 0, this.width, this.height);
            
            // 获取图像的base64编码
            var decode = this.canvas.toDataURL('image/jpeg', 0.8);
            console.log("图像捕获成功");
            return decode;
        } catch (e) {
            console.error("获取图像失败:", e);
            alert("获取图像失败: " + e.message);
            return null;
        }
    },
    
    // 关闭摄像头
    closeVideo: function() {
        if (this.video && this.video.srcObject) {
            let tracks = this.video.srcObject.getTracks();
            tracks.forEach(function(track) {
                track.stop();
            });
            this.video.srcObject = null;
            this.isOpen = false;
            console.log("摄像头已关闭");
        }
    }
}


