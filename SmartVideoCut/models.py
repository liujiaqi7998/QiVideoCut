import os
import uuid
from datetime import timezone, datetime

from django.db import models
from django import forms
from django.utils.html import format_html


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



