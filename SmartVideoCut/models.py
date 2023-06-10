import os
import threading
from tkinter import Image

import cv2
import numpy as np
import numpy as nps
from django.db import models
from imutils.object_detection import non_max_suppression
from loguru import logger

from QiVideoCut.settings import Update_ROOT, Watermark_TEXT


class video_status_db(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.TextField(verbose_name="用户名")
    file_uuid = models.TextField(verbose_name="文件UUID")
    file_raw_name = models.TextField(verbose_name="原始文件名")
    status = models.IntegerField(verbose_name="状态")
    Task_PID = models.IntegerField(verbose_name="线程PID", default=-1)
    message = models.TextField(verbose_name="通知信息")

    def __str__(self):
        return self.file_raw_name

    # 用于给本表指定一个别名
    class Meta:
        verbose_name = "管理转换列表"
        verbose_name_plural = "管理转换列表"

    # 自定义方法,主要负责给主机标注颜色
    def Status(self):
        if self == -1:
            format_td = "错误"
        if self == 0:
            format_td = "上传中"
        elif self == 1:
            format_td = "上传完成准备就绪"
        elif self == 2:
            format_td = "分析中"
        elif self == 3:
            format_td = "剪辑中"
        elif self == 4:
            format_td = "合成中"
        elif self == 5:
            format_td = "完成"
        elif self == 6:
            format_td = "终止"
        else:
            format_td = "未知"
        return format_td


All_Thread = {}


class solve_video_Thread(threading.Thread):

    def __init__(self, threadId, name):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.isRun = True

    def run(self):
        file_uuid = self.name
        logger.info(f'开始线程：{file_uuid}')

        temp_db = video_status_db.objects.get(file_uuid=file_uuid)  # 获取id为3的作者对象
        temp_db.status = 3
        temp_db.message = video_status_db.Status(temp_db.status)
        temp_db.Task_PID = temp_db.id
        temp_db.save()
        All_Thread[temp_db.Task_PID] = self

        Raw_video_uri = os.path.join(Update_ROOT, 'Raw_video')
        Raw_video_file_uuid_uri = os.path.join(Raw_video_uri, file_uuid + ".mp4")

        Out_Video_uri = os.path.join(Update_ROOT, 'Out_Video')
        Out_Video_file_uuid_uri = os.path.join(Out_Video_uri, file_uuid + ".mp4")

        Watermark_file_uuid_uri = os.path.join(Update_ROOT, "watermark.png")
        # Watermark = cv2.imread(Watermark_file_uuid_uri)

        if not os.path.exists(Raw_video_file_uuid_uri):
            temp_db = video_status_db.objects.get(file_uuid=file_uuid)  # 获取id为3的作者对象
            temp_db.status = 0
            temp_db.message = "读取视频错误：文件不存在"
            temp_db.save()
            logger.error(f'提取视频：{file_uuid}，时发送错误：文件不存在')
            return

        # 初始化方向梯度直方图描述子
        hog = cv2.HOGDescriptor()
        # 设置支持向量机使得它成为一个预先训练好了的行人检测器
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        try:
            # 读取摄像头视频
            capture = cv2.VideoCapture(Raw_video_file_uuid_uri)
        except Exception as err:
            temp_db = video_status_db.objects.get(file_uuid=file_uuid)  # 获取id为3的作者对象
            temp_db.status = -1
            temp_db.message = f"读取视频错误：{err}"
            temp_db.save()
            logger.error(f'提取视频：{file_uuid}，时发送错误：读取视频错误：{err}')
            return

        frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_rate = float(capture.get(5))  # 拉帧率
        frame_all_num = int(capture.get(7))  # 全部帧数
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(Out_Video_file_uuid_uri, fourcc, frame_rate, (frame_width, frame_height), True)

        ret = 1
        if capture.isOpened():
            m = 0
            while ret:
                if not self.isRun:
                    break
                ret, img = capture.read()  # img 就是一帧图片
                if not ret: break
                try:
                    # 可以用 cv2.imshow() 查看这一帧，也可以逐帧保存
                    check_img = cv2.resize(img, (int(frame_height / 4), int(frame_width / 4)))
                    # 通过调用detectMultiScale的hog描述子方法，对图像中的行人进行检测。
                    (rects, weights) = hog.detectMultiScale(check_img, winStride=(4, 4), padding=(8, 8), scale=1.05)
                    # 应用非极大值抑制，通过设置一个阈值来抑制重叠的框。
                    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
                    pick = non_max_suppression(rects, overlapThresh=0.65)
                    # 绘制红色人体矩形框
                    if len(pick) >= 1:
                        cv2.putText(img, Watermark_TEXT, (10,25), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 1)
                        writer.write(img)
                        cv2.imshow("wname", img)
                except Exception as err:
                    logger.error(f'提取视频：{file_uuid}，时发送错误：读取视频错误：{err}')
                    pass
                m = m + 1
                temp_db = video_status_db.objects.get(file_uuid=file_uuid)  # 获取id为3的作者对象
                temp_db.message = f'{m}/{frame_all_num}'
                temp_db.save()
        # 释放资源
        capture.release()
        writer.release()
        temp_db = video_status_db.objects.get(file_uuid=self.name)  # 获取id为3的作者对象
        temp_db.status = 5
        temp_db.message = video_status_db.Status(temp_db.status)
        temp_db.save()
        logger.info(f'转换完成，结束线程：{self.name}')

    def __del__(self):
        logger.info(f'结束线程：{self.name}')

    def stop(self):
        temp_db = video_status_db.objects.get(file_uuid=self.name)  # 获取id为3的作者对象
        temp_db.status = 6
        temp_db.message = video_status_db.Status(temp_db.status)
        temp_db.save()
        logger.info(f'强制结束线程：{self.threadId}')
        self.isRun = False
