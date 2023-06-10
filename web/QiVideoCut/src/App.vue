<template>
  <div class="navbar" >
    <div class="left-side">
      <a-space>
        <img
            alt="logo"
            src="//s1.ax1x.com/2023/06/07/pCF2rdO.png"
            :style="{ width: '50px', }"
        />
        <a-typography-title :style="{ margin: 0, fontSize: '18px' }" :heading="5">
          易滑邦 —— 智能快剪
        </a-typography-title>
      </a-space>
    </div>
  </div>

  <a-config-provider>
    <router-view />
  </a-config-provider>
</template>

<style>
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    height: 60px;
    background-color:rgba(255,255,255,0.5);
    box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.15);
  }


body {
  background-image: url("https://api.1314.cool/bingimg");
}
</style>