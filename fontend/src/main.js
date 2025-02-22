import { createApp } from "vue";
import NProgress from "nprogress";
import App from "./App.vue";

import "nprogress/nprogress.css";
import "./style.scss";

import { createWebHistory, createRouter } from "vue-router";

const routes = [
    { path: "/", name: "home", component: () => import("@/views/HomeView.vue") },
    { path: "/create", name: "create", component: () => import("@/views/CreateView.vue") },
    { path: "/library", name: "library", component: () => import("@/views/LibraryView.vue") },
    { path: "/search", name: "search", component: () => import("@/views/SearchView.vue") },
    { path: "/track/:id", name: "track", component: () => import("@/views/TrackView.vue") },
    { path: "/playlist/:id", name: "playlist", component: () => import("@/views/PlaylistView.vue") },
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
    next();
});

router.afterEach(() => {
    NProgress.done();
});

createApp(App).use(router).mount("#app");
