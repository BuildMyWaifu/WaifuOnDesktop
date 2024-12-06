/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { useAppStore } from "@/stores/app";
import { fetchApi } from "@/utils/api";
import { createRouter, createWebHistory } from "vue-router/auto";
import { getCookie } from "@/utils/utils";

const routes = [
  {
    path: "/",
    component: () => import("@/pages/index.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/app",
    name: "Home",
    component: () => import("@/pages/Main.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "Login",
    meta: { requiresAuth: false },
    component: () => import("@/pages/Login.vue"),
  },
  {
    path: "/signup",
    name: "SignUp",
    meta: { requiresAuth: false },
    component: () => import("@/pages/SignUp.vue"),
  },
  {
    path: "/test",
    name: "Test",
    meta: { requiresAuth: false },
    component: () => import("@/pages/TestPage.vue"),
  },
  {
    path: "/:pathMatch(.*)*",
    name: "Error",
    meta: { requiresAuth: false },
    component: () => import("@/pages/ErrorPage.vue"),
  },
  {
    path: "/liveChat",
    name: "LiveChat",
    meta: { requiresAuth: false },
    component: () => import("@/pages/LiveChatPage.vue"), // Ensure the casing matches
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.("Failed to fetch dynamically imported module")) {
    if (!localStorage.getItem("vuetify:dynamic-reload")) {
      console.log("Reloading page to fix dynamic import error");
      localStorage.setItem("vuetify:dynamic-reload", "true");
      location.assign(to.fullPath);
    } else {
      console.error("Dynamic import error, reloading page did not fix it", err);
    }
  } else {
    console.error(err);
  }
});

router.isReady().then(() => {
  localStorage.removeItem("vuetify:dynamic-reload");
});

router.beforeEach(async function (to) {
  const store = useAppStore();
  if (to.meta.requiresAuth && !store.user) {
    const res = await fetchApi("/me");
    if (res.status == "success") {
      store.login(res.data);
    } else {
      if (getCookie("token").length > 0) {
        alert("登入已過期！請重新登入");
      } else {
        alert("您尚未登入！此頁面登入後方可閱覽");
      }
      return {
        path: "/login",
        query: { redirect: to.fullPath },
      };
    }
  }
});

export default router;
