<template>
  <a-card id="main-card" title="开启智能制作之旅" hoverable>
    <a-button type="primary" long @click="go_more">查看更多</a-button>
    <br>
    <a-upload
        draggable
        :with-credentials=true
        :show-remove-button=false
        :action="`/api_v1/upload`"
        :limit="1"
        accept=".mp4"
        @success="uploadSuccess"
        @error="uploadError"
    />
    <div v-show="show_uuid">
      <h2>文件密钥，请妥善保管</h2>
      <h2 id="show_file_uuid">{{ file_uuid }}</h2>
      <a-button type="primary" long @click="check_status_butt">获取转换状态</a-button>
    </div>
  </a-card>
  <a-modal v-model:visible="visible" @ok="onRest" @cancel="onRest">
    <template #title>
      提示
    </template>
    <div>{{ tipMsg }}</div>
  </a-modal>
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

#show_file_uuid {
  color: #3f0063;
  border-style: dotted;
  border-width: 4px;
  border-color: green;
  padding: 8px 1px 8px 1px;
}
</style>


<script lang="ts">
import {reactive} from 'vue';
import VueRouter from 'vue-router'
import {Router} from 'vue-router';

export default {
  data() {
    return {
      tipMsg: "",
      visible: false,
      show_uuid: false,
      file_uuid: "获取失败，请重新上传"
    }
  },
  setup() {
    return {
    }
  },

  methods: {
    uploadSuccess(r: any) {
      const ResResult = JSON.parse(r.response)
      console.log(ResResult)
      if (ResResult.code <= 0) {
        this.tipMsg = ResResult.msg
        this.visible = true
        return;
      }
      this.file_uuid = ResResult.uuid
      this.show_uuid = true
    },
    uploadError() {
      this.tipMsg = "文件上传错误，请重新上传！"
      this.visible = true
    },
    check_status_butt(){
      console.log("获取转换状态按钮按下")
      this.$router.push({
          name:'status',
          params:{
            file_uuid:this.file_uuid
          }
      })
    },
    onRest() {
      window.location.reload()
    },
    go_more(){
      this.$router.push({
          name:'get'
      })
    }
  }
}
</script>