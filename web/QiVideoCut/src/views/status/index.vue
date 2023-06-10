<template>
  <a-card id="main-card" title="剪辑状态" hoverable>


    <a-form :model="formData" >

        <a-form-item field="user_name" label="用户名">
          <a-input
              readonly
            v-model="formData.user_name"
          />
        </a-form-item>

        <a-form-item field="file_uuid" label="文件密钥">
            <a-input
                readonly
              v-model="formData.file_uuid"
            />
        </a-form-item>

        <a-form-item field="file_raw_name" label="原始文件名">
            <a-input
                readonly
              v-model="formData.file_raw_name"
            />
        </a-form-item>

         <a-form-item field="status_name" label="状态">
            <a-input
                readonly
              v-model="formData.status_name"
            />
         </a-form-item>

        <a-form-item field="message" label="信息">
            <a-input
                readonly
              v-model="formData.message"
            />
        </a-form-item>

      <a-progress
      :percent=percent
      :color="{
        '0%': 'rgb(var(--primary-6))',
        '100%': 'rgb(var(--success-6))',
      }"
    />
      <br>

        <a-form-item>
          <a-space>
            <a-button @click="get_back" >返回</a-button>
            <a-button v-show="can_download" @click="get_download" status="success">下载文件</a-button>
            <a-button @click="Delete_button" status="danger">停止转换并删除</a-button>
          </a-space>
        </a-form-item>
    </a-form>
  </a-card>
</template>

<style>
#main-card {
  text-align: center;
  background-color: #fff;
  border-radius: 20px;
  width: 500px;
  height: 450px;
  margin: auto;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

</style>


<script lang="ts">
import {reactive} from 'vue';
import VueRouter from 'vue-router'
import {Router} from 'vue-router';
import axios from 'axios'
import { Modal } from '@arco-design/web-vue';

export default {
  data() {
    return {
      tipMsg: "",
      visible: false,
      show_uuid: false,
      file_uuid: "获取失败，请重新上传",
      Host: "/api_v1",
      can_download: false,
      formData: {
        code: -999,
        user_name: "",
        file_uuid : String(this.$route.params.file_uuid),
        file_raw_name: "",
        status: -1,
        status_name: "",
        Task_PID: "",
        message: "",
        msg: ""
      },
      intervalBox: 0,
      percent: 0
    }
  },
  mounted() {
    this.TimeDo();
    this.intervalBox = window.setInterval(() => {
      this.TimeDo()
    }, 3000);
  },
  setup() {
    return {
    }
  },

  methods: {
    get_back(){
      window.clearInterval(this.intervalBox);
      window.history.back();
    },
    async TimeDo() {
      try {
        const res = await axios.get(`${this.Host}/get_status/${this.formData.file_uuid}`)
        this.formData = JSON.parse(res.request.response)
        if(this.formData.code <= 0){
          window.clearInterval(this.intervalBox);
          Modal.info({
            title: '提示',
            content: `${this.formData.msg}`,
            onClose: this.get_back,
          });
          return
        }
        this.percent = 0
        this.can_download = false
        if(this.formData.status === -1){
          this.formData.status_name = "错误"
        }
        else if(this.formData.status === 0){
          this.formData.status_name = "上传中"
        }
        else if(this.formData.status === 1){
          this.formData.status_name = "上传完成准备就绪"
        }
        else if(this.formData.status === 2){
          this.formData.status_name = "分析中"
        }
        else if(this.formData.status === 3){
          this.formData.status_name = "剪辑中"
          const arr = this.formData.message.split('/');
          this.percent = parseFloat((parseFloat(arr[0])/parseFloat(arr[1])).toFixed(3))
        }
        else if(this.formData.status === 4){
          this.formData.status_name = "合成中"
        }
        else if(this.formData.status === 5){
          this.formData.status_name = "完成"
          this.can_download = true
          this.percent = 1
        }
        else if(this.formData.status === 6){
          this.formData.status_name = "终止"
        }
      } catch (e: any) {
        window.clearInterval(this.intervalBox);
        if (e.response.status === 404){
          e.message = "文件密钥不正确"
        }
        Modal.error({
          title: '提示',
          content: `${e.message}`,
          onClose: this.get_back,
        });
      }
    },
    onRest () {
      this.get_back();
    },
    get_download(){
      window.open(`${this.Host}/download/${this.formData.file_uuid}`, '_blank');
    },
     async Delete_button() {
      try {
        const res = await axios.get(`${this.Host}/stop_solve/${this.formData.file_uuid}`, {
          withCredentials: true
        })
        this.TimeDo()
        const ResResult = JSON.parse(res.request.response)
        Modal.info({
          title: '提示',
          content: `${ResResult.msg}`
        });
      } catch (e: any) {
        Modal.error({
          title: '提示',
          content: `${e.message}`
        });
      }
    },
  },
}
</script>