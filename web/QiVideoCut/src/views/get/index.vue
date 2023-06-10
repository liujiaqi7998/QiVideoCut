<template>
  <a-card id="main-card" title="更多" hoverable>
    <h2>查看文件处理进度</h2>
    <a-form :model="formData">
        <a-form-item field="user_name" label="文件密钥" :rules="[{required:true,message:'请填写文件密钥'}]">
          <a-input
            v-model="file_uuid"
          />
        </a-form-item>
        <a-form-item>
          <a-space>
            <a-button @click="get_back" >返回</a-button>
            <a-button @click="get_status" status="success" html-type="submit">获取转换状态</a-button>
            <a-button @click="go_admin" status="warning">登录管理后台</a-button>
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
      file_uuid: "",
      Host: "",
      can_download: false,
      formData: {}
    }
  },

  setup() {
    return {
    }
  },

  methods: {
    get_status(){
      this.$router.push({
          name:'status',
          params:{
            file_uuid:this.file_uuid
          }
      })
    },
    go_admin(){
      window.open(`${this.Host}/admin/`, '_blank');
    },
    get_back(){
      this.$router.push({
          name:'index'
      })
    }
  }
}
</script>