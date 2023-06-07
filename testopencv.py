import os

import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
import imutils

# # 初始化方向梯度直方图描述子
# hog = cv2.HOGDescriptor()
# # 设置支持向量机使得它成为一个预先训练好了的行人检测器
# hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
# # 读取摄像头视频
# cap = cv2.VideoCapture('123.mp4')
#
# while True:
#     # 按帧读取视频
#
#     ret, img = cap.read()
#     img = cv2.resize(img, (320, 180))
#     # 将每一帧图像ROI区域抠出来
#     # img_roi = img1[img_roi_y:(img_roi_y + img_roi_height), img_roi_x:(img_roi_x + img_roi_width)]
#     roi = img
#     # 通过调用detectMultiScale的hog描述子方法，对图像中的行人进行检测。
#     (rects, weights) = hog.detectMultiScale(roi, winStride=(4, 4), padding=(8, 8), scale=1.05)
#     # 应用非极大值抑制，通过设置一个阈值来抑制重叠的框。
#     rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
#     pick = non_max_suppression(rects, overlapThresh=0.65)
#     # 绘制红色人体矩形框
#     for (x, y, w, h) in pick:
#         cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 2)
#     # 打印检测到的目标个数
#     print("检测到进入危险区域行人个数为{}".format(len(pick)))
#     # 展示每一帧图像
#     if len(pick) >= 1 :
#         cv2.imshow("HOG+SVM+NMS", img)
#     # 按esc键退出循环
#     if cv2.waitKey(1) & 0xff == 27:
#         break
#
# # 释放资源
# cap.release()
# cv2.destroyAllWindows()
from QiVideoCut.settings import Update_ROOT

print("开始线程")
file_uuid = "123"

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
        print(f'{m}/{frame_all_num}')

# 释放资源
capture.release()
writer.release()
