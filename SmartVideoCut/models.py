import os
import threading
import uuid
from datetime import timezone, datetime
from imutils.object_detection import non_max_suppression

import cv2
import numpy as np
from django.db import models
from django import forms
from django.utils.html import format_html

from QiVideoCut.settings import Update_ROOT


class video_status_db(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.TextField(verbose_name="用户名")
    file_uuid = models.TextField(verbose_name="文件UUID")
    file_raw_name = models.TextField(verbose_name="原始文件名")
    status = models.IntegerField(verbose_name="状态")
    Task_PID = models.IntegerField(verbose_name="线程PID")
    message = models.TextField(verbose_name="通知信息")

    def __str__(self):
        return self.file_raw_name

    # 用于给本表指定一个别名
    class Meta:
        verbose_name = "管理转换列表"
        verbose_name_plural = "管理转换列表"

    # 自定义方法,主要负责给主机标注颜色
    def Status(self):
        if self.status == -1:
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">错误</span>')
        if self.status == 0:
            format_td = format_html('<span style="padding:2px;background-color:yellow;color:white">上传中</span>')
        elif self.status == 1:
            format_td = format_html('<span style="padding:2px;background-color:yellow;color:black">转换中</span>')
        elif self.status == 2:
            format_td = format_html('<span style="padding:2px;background-color:green;color:white">分析中</span>')
        elif self.status == 3:
            format_td = format_html('<span style="padding:2px;background-color:green;color:white">剪辑中</span>')
        elif self.status == 4:
            format_td = format_html('<span style="padding:2px;background-color:green;color:white">合成中</span>')
        elif self.status == 5:
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">完成</span>')
        else:
            format_td = format_html('<span style="padding:2px;background-color:black;color:white">未知</span>')
        return format_td


class del_video_Thread(threading.Thread):
    def __init__(self, threadId, name, counter):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.counter = counter

    def run(self):
        file_uuid = self.name
        print(f'开始线程{file_uuid}')
        temp_db = video_status_db.objects.get(file_uuid=file_uuid)  # 获取id为3的作者对象
        temp_db.status = 3
        temp_db.save()

        Raw_video_uri = os.path.join(Update_ROOT, 'Raw_video')
        Raw_video_file_uuid_uri = os.path.join(Raw_video_uri, file_uuid + ".mp4")

        Out_Video_uri = os.path.join(Update_ROOT, 'Out_Video')
        Out_Video_file_uuid_uri = os.path.join(Out_Video_uri, file_uuid + ".mp4")

        Watermark_file_uuid_uri = os.path.join(Update_ROOT, "watermark.png")

        # 初始化方向梯度直方图描述子
        hog = cv2.HOGDescriptor()
        # 设置支持向量机使得它成为一个预先训练好了的行人检测器
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        # 读取摄像头视频
        capture = cv2.VideoCapture(Raw_video_file_uuid_uri)

        frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_rate = float(capture.get(5))  # 拉帧率
        frame_all_num = int(capture.get(7))  # 全部帧数
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(Out_Video_file_uuid_uri, fourcc, frame_rate, (frame_width, frame_height), True)

        watermark = cv2.imread(Watermark_file_uuid_uri)

        ret = 1
        if capture.isOpened():
            m = 0
            while ret:
                ret, img = capture.read()  # img 就是一帧图片
                # 可以用 cv2.imshow() 查看这一帧，也可以逐帧保存
                check_img = cv2.resize(img, (320, 180))
                # 通过调用detectMultiScale的hog描述子方法，对图像中的行人进行检测。
                (rects, weights) = hog.detectMultiScale(check_img, winStride=(4, 4), padding=(8, 8), scale=1.05)
                # 应用非极大值抑制，通过设置一个阈值来抑制重叠的框。
                rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
                pick = non_max_suppression(rects, overlapThresh=0.65)
                # 绘制红色人体矩形框
                if len(pick) >= 1:
                    writer.write(img)

                m = m + 1
                temp_db = video_status_db.objects.get(file_uuid=file_uuid)  # 获取id为3的作者对象
                temp_db.message = f'{m}/{frame_all_num}'
                temp_db.save()

        # 释放资源
        capture.release()
        writer.release()

    def __del__(self):
        print("线程结束！")
