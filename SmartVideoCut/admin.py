from django.contrib import admin

# Create your models here.
from SmartVideoCut.models import video_status_db

admin.site.site_header = '易滑邦快剪管理平台'  # 设置header
admin.site.site_title = '易滑邦快剪管理平台'  # 设置title


# 必须继承ModelAdmin基类,才可以调整参数,HostDB则是你的表的名称
@admin.register(video_status_db)
class MyAdmin(admin.ModelAdmin):
    # list_display = 你需要展示的字段应该写在这里,此处是数据库中的字段
    list_display = ("user_name", "file_uuid", "file_raw_name", "status", "Task_PID", "message")
    search_fields = ("file_uuid", "user_name")
    list_filter = ("user_name", "status")
    # ordering = 设置一个排序条件,此处是以id作为排序依据
    ordering = ("id",)
    # list_per_page = 设置每页显示多少条记录,默认是100条
    list_per_page = 10

