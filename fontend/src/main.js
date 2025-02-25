import { createApp } from "vue";
import NProgress from "nprogress";
import App from "./App.vue";

import "nprogress/nprogress.css";
import "./style.scss";

import { createWebHistory, createRouter } from "vue-router";

const routes = [
    {
        path: "/",
        name: "home",
        component: () => import("@/views/HomeView.vue"),
    },
    {
        path: "/login",
        name: "login",
        component: () => import("@/views/LoginView.vue"),
        meta: { hideSidebar: true },
    },
    {
        path: "/register",
        name: "register",
        component: () => import("@/views/RegisterView.vue"),
        meta: { hideSidebar: true },
    },
    {
        path: "/create",
        name: "create",
        component: () => import("@/views/CreateView.vue"),
        meta: { requiresAuth: true },
    },
    {
        path: "/library",
        name: "library",
        component: () => import("@/views/LibraryView.vue"),
        meta: { requiresAuth: true },
    },
    {
        path: "/search",
        name: "search",
        component: () => import("@/views/SearchView.vue"),
    },
    {
        path: "/track/:id",
        name: "track",
        component: () => import("@/views/TrackView.vue"),
    },
    {
        path: "/playlist/:id",
        name: "playlist",
        component: () => import("@/views/PlaylistView.vue"),
    },
    {
        path: "/:pathMatch(.*)*",
        component: () => import("@/views/PageNotView.vue"),
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

NProgress.configure({ showSpinner: false });

router.beforeEach((to, from, next) => {
    NProgress.start();
    const token = localStorage.getItem("token");
    if (to.meta.requiresAuth && !token) {
        next({ path: "/login", query: { redirect: to.fullPath } });
    } else {
        next();
    }
});

router.afterEach(() => {
    NProgress.done();
});

createApp(App).use(router).mount("#app");
