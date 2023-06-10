import json
import os
import time
import uuid

from django.utils.encoding import escape_uri_path
from loguru import logger
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from QiVideoCut.settings import Update_ROOT
from SmartVideoCut import models
from SmartVideoCut.models import video_status_db, solve_video_Thread


def index(request):
    # return redirect("index:shop",permanent=True)
    return render(request, "index.html")


@logger.catch
def upload(request):
    # 请求方法为POST时，执行文件上传
    back_data = {
        "code": -5000,
        "msg": "未知错误"
    }
    if request.method == "POST":
        myFile = request.FILES.get("file", None)
        if not myFile:
            back_data = {
                "code": -1002,
                "msg": "未发现上传文件"
            }
            logger.error(f"调用上传方法，但是没有携带文件")
            return HttpResponse(json.dumps(back_data))

        # 随机生成UUID
        file_uuid = str(uuid.uuid4())
        Raw_video_uri = os.path.join(Update_ROOT, 'Raw_video')
        Raw_video_file_uuid_uri = os.path.join(Raw_video_uri, file_uuid + ".mp4")

        logger.info(f"接收到上传文件，保存到：{Raw_video_file_uuid_uri}")

        video_status_db.objects.create(
            user_name="",
            file_uuid=file_uuid,
            file_raw_name=myFile.name,
            status=0,
            Task_PID=0,
            message=video_status_db.Status(0)
        )

        try:
            # 打开特定的文件进行二进制的写操作
            f = open(Raw_video_file_uuid_uri, "wb+")
            # 分块写入文件
            for chunk in myFile.chunks():
                f.write(chunk)
            f.close()
        except Exception as err:
            logger.error(f'保存上传文件：{Raw_video_file_uuid_uri}，时发送错误：{err}')
            temp_db = video_status_db.objects.get(file_uuid=file_uuid)  # 获取id为3的作者对象
            temp_db.status = -1
            temp_db.message = "保存上传文件失败，请重试"
            temp_db.save()
            back_data = {
                "code": -1003,
                "msg": "保存上传文件失败，请重试",
                "uuid": file_uuid
            }
            return HttpResponse(json.dumps(back_data))
            pass

        temp_db = video_status_db.objects.get(file_uuid=file_uuid)  # 获取id为3的作者对象
        temp_db.status = 1
        temp_db.message = video_status_db.Status(temp_db.status)
        temp_db.save()

        solve_video_Thread(temp_db.id, file_uuid).start()
        back_data = {
            "code": 1,
            "msg": "上传成功",
            "uuid": file_uuid
        }
        return HttpResponse(json.dumps(back_data))
    else:
        # 请求方法为get时，生成文件上传页面
        back_data = {
            "code": -1001,
            "msg": "请使用Post方法提交文件"
        }
        logger.info(f"调用上传方法，使用的是GET方法")
        return HttpResponse(json.dumps(back_data))


@logger.catch
def get_status(request, file_uuid):
    if request.method == "GET":
        file_uuid = str(file_uuid)
        temp_db = video_status_db.objects.filter(file_uuid=file_uuid)
        if temp_db.exists():
            temp_db = temp_db.get()
            back_data = {
                "code": 1,
                "msg": "获取成功",
                "user_name": temp_db.user_name,
                "file_uuid": temp_db.file_uuid,
                "file_raw_name": temp_db.file_raw_name,
                "status": temp_db.status,
                "Task_PID ": temp_db.Task_PID,
                "message": temp_db.message
            }
            logger.info(f"调用查询状态接口，查询UUID：{file_uuid}")
            return HttpResponse(json.dumps(back_data))
        else:
            back_data = {
                "code": 0,
                "msg": "文件不存在",
                "file_uuid": file_uuid
            }
            logger.info(f"调用查询状态接口，但是没UUID：{file_uuid} 没有查到")
            return HttpResponse(json.dumps(back_data))
        pass
    else:
        # 请求方法为get时，生成文件上传页面
        back_data = {
            "code": -1001,
            "msg": "请使用Get方法查看文件状态"
        }
        logger.info(f"调用查询状态接口，使用的是Post方法")
        return HttpResponse(json.dumps(back_data))


@logger.catch
def stop_solve(request, file_uuid):
    if request.method == "GET":
        file_uuid = str(file_uuid)
        temp_db = video_status_db.objects.filter(file_uuid=file_uuid)
        if temp_db.exists():
            temp_db = temp_db.get()
            if temp_db.status == 6:
                back_data = {
                    "code": 1,
                    "msg": "已经是停止状态",
                    "file_uuid": temp_db.file_uuid,
                }
                logger.info(f"调用删除状态接口，删除UUID：{file_uuid}，但是文件已经删除")
                return HttpResponse(json.dumps(back_data))
            if temp_db.Task_PID != 0:
                logger.debug("检测到删除的UUID存在转换业务，强行停止任务")
                try:
                    temp_Thread = models.All_Thread[temp_db.Task_PID]
                    if temp_Thread:
                        logger.debug("强行停止任务")
                        temp_Thread.stop()
                        time.sleep(1)
                except Exception as err:
                    logger.info(f"调用删除状态接口，删除UUID：{file_uuid}，但是线程停止失败了，原因是：{err}")

            Raw_video_uri = os.path.join(Update_ROOT, 'Raw_video')
            Raw_video_file_uuid_uri = os.path.join(Raw_video_uri, file_uuid + ".mp4")

            Out_Video_uri = os.path.join(Update_ROOT, 'Out_Video')
            Out_Video_file_uuid_uri = os.path.join(Out_Video_uri, file_uuid + ".mp4")

            if os.path.exists(Raw_video_file_uuid_uri):
                os.remove(Raw_video_file_uuid_uri)
            if os.path.exists(Out_Video_file_uuid_uri):
                os.remove(Out_Video_file_uuid_uri)

            back_data = {
                "code": 1,
                "msg": "删除成功",
                "file_uuid": temp_db.file_uuid,
            }
            logger.info(f"调用删除状态接口，删除UUID：{file_uuid}")
            return HttpResponse(json.dumps(back_data))
        else:
            back_data = {
                "code": 0,
                "msg": "文件不存在",
                "file_uuid": file_uuid
            }
            logger.info(f"调用删除状态接口，但是没UUID：{file_uuid} 没有查到")
            return HttpResponse(json.dumps(back_data))
        pass
    else:
        # 请求方法为get时，生成文件上传页面
        back_data = {
            "code": -1001,
            "msg": "请使用Get方法查看文件状态"
        }
        logger.info(f"调用删除状态接口，使用的是Post方法")
        return HttpResponse(json.dumps(back_data))


@logger.catch
def download(request, file_uuid):
    if request.method == "GET":
        file_uuid = str(file_uuid)
        Out_Video_uri = os.path.join(Update_ROOT, 'Out_Video')
        Out_Video_file_uuid_uri = os.path.join(Out_Video_uri, file_uuid + ".mp4")
        # 判断文件是否存在
        if os.path.exists(Out_Video_file_uuid_uri):
            temp_db = video_status_db.objects.get(file_uuid=file_uuid)  # 获取id为3的作者对象
            file = open(Out_Video_file_uuid_uri, 'rb')
            response = HttpResponse(file)
            response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
            logger.info(f"下载文件：{temp_db.file_raw_name},uuid：{file_uuid}")
            out_file_name = str(f'易滑邦快剪_{temp_db.file_raw_name}')
            response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(out_file_name))
            return response
        else:
            back_data = {
                "code": 0,
                "msg": "文件不存在",
                "file_uuid": file_uuid
            }
            logger.info(f"调用下载接口，但是没UUID：{file_uuid} 没有查到")
            return HttpResponse(json.dumps(back_data))
    else:
        # 请求方法为get时，生成文件上传页面
        back_data = {
            "code": -1001,
            "msg": "请使用Get方法查看文件状态"
        }
        logger.info(f"调用删除状态接口，使用的是Post方法")
        return HttpResponse(json.dumps(back_data))
