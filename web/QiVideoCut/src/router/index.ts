import { createRouter, createWebHistory } from 'vue-router';
import NProgress from 'nprogress'; // progress bar
import 'nprogress/nprogress.css';


NProgress.configure({ showSpinner: false }); // NProgress Configuration

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: 'index',
    },
    {
      path: '/status',
      redirect: 'status/0',
    },
    {
      path: '/index',
      name: 'index',
      component: () => import('@/views/index/index.vue'),
      meta: {
        requiresAuth: false,
      },
    },
      {
      path: '/status/:file_uuid',
      name: 'status',
      component: () => import('@/views/status/index.vue'),
      meta: {
        requiresAuth: false,
      },
    },
      {
      path: '/get',
      name: 'get',
      component: () => import('@/views/get/index.vue'),
      meta: {
        requiresAuth: false,
      },
    }
  ],
  scrollBehavior() {
    return { top: 0 };
  },
});

export default router;
