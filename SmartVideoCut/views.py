import uuid

from MySQLdb.constants.FIELD_TYPE import NULL
from django.shortcuts import render
from django.http import HttpResponse

import os

# Create your views here.
from QiVideoCut.settings import Update_ROOT
from SmartVideoCut.models import video_status_db


def index(request):
    # return redirect("index:shop",permanent=True)
    return render(request, "index.html")


def upload(request):
    # 请求方法为POST时，执行文件上传
    if request.method == "POST":
        myFile = request.FILES.get("file", None)
        if not myFile:
            return HttpResponse("no files for upload")

        # 随机生成UUID
        file_uuid = str(uuid.uuid4())
        Raw_video_uri = os.path.join(Update_ROOT, 'Raw_video')
        Raw_video_file_uuid_uri = os.path.join(Raw_video_uri, file_uuid + ".mp4")
        print(Raw_video_file_uuid_uri)

        video_status_db.objects.create(
            user_name="",
            file_uuid=file_uuid,
            file_raw_name=myFile.name,
            status=0,
            Task_PID=0,
            message="上传中"
        )

        # 打开特定的文件进行二进制的写操作
        f = open(Raw_video_file_uuid_uri, "wb+")
        # 分块写入文件
        for chunk in myFile.chunks():
            f.write(chunk)
        f.close()

        return HttpResponse(file_uuid)
    else:
        # 请求方法为get时，生成文件上传页面
        return render(request, "index.html")
