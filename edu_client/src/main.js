// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import "element-ui/lib/theme-chalk/index.css"
// 导入全局样式
import "../static/css/global.css"

// 配置域名
import settings from "./settings";

Vue.prototype.$settings = settings

// 配置视频播放
require('video.js/dist/video-js.css');
require('vue-video-player/src/custom-theme.css');
import VideoPlayer from 'vue-video-player'

Vue.use(VideoPlayer);
// 配置axios
import axios from 'axios'

import '../static/js/gt'

Vue.prototype.$axios = axios
// 全局注册
Vue.use(ElementUI)

Vue.config.productionTip = false

import store from "./store/index";
/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    components: {App},
    template: '<App/>',
    store,
})
