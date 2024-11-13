/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router/auto'

const routes = [
  {
    path: '/',
    component: () => import('@/pages/index.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/app',
    name: 'Home',
    component: () => import('@/pages/Main.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    meta: { requiresAuth: false },
    component: () => import('@/pages/Login.vue'),
  },
  {
    path: '/signup',
    name: 'SignUp',
    meta: { requiresAuth: false },
    component: () => import('@/pages/SignUp.vue'),
  },
  {
    path: '/test',
    name: 'Test',
    meta: { requiresAuth: false },
    component: () => import('@/pages/TestPage.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'Error',
    meta: { requiresAuth: false },
    component: () => import('@/pages/ErrorPage.vue'),
  },
  {
    path: '/newWife',
    name: 'CreateNewWife',
    meta: { requiresAuth: false },
    component: () => import('@/pages/CreateNewWife.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (!localStorage.getItem('vuetify:dynamic-reload')) {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    } else {
      console.error('Dynamic import error, reloading page did not fix it', err)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router
