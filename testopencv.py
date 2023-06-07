import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
import imutils

# 初始化方向梯度直方图描述子
hog = cv2.HOGDescriptor()
# 设置支持向量机使得它成为一个预先训练好了的行人检测器
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
# 读取摄像头视频
cap = cv2.VideoCapture('123.mp4')

while True:
    # 按帧读取视频

    ret, img = cap.read()
    img = cv2.resize(img, (320, 180))
    # 将每一帧图像ROI区域抠出来
    # img_roi = img1[img_roi_y:(img_roi_y + img_roi_height), img_roi_x:(img_roi_x + img_roi_width)]
    roi = img
    # 通过调用detectMultiScale的hog描述子方法，对图像中的行人进行检测。
    (rects, weights) = hog.detectMultiScale(roi, winStride=(4, 4), padding=(8, 8), scale=1.05)
    # 应用非极大值抑制，通过设置一个阈值来抑制重叠的框。
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, overlapThresh=0.65)
    # 绘制红色人体矩形框
    for (x, y, w, h) in pick:
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 2)
    # 打印检测到的目标个数
    print("检测到进入危险区域行人个数为{}".format(len(pick)))
    # 展示每一帧图像
    if len(pick) >= 1 :
        cv2.imshow("HOG+SVM+NMS", img)
    # 按esc键退出循环
    if cv2.waitKey(1) & 0xff == 27:
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
