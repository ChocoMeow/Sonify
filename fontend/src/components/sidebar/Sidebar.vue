<template>
    <aside>
        <router-link :to="{ name: home }" class="logo">
            <img :src="logoURL" alt="" />
            <p>Sonify</p>
        </router-link>

        <div class="menu">
            <SidebarBtn icon="home" name="Home" />
            <SidebarBtn icon="music_note_add" name="Create" />
            <SidebarBtn icon="bookmarks" name="Library" />
        </div>

        <div class="flex"></div>

        <div class="menu">
            <!-- <SidebarBtn icon="help" name="Support" /> -->
            <SidebarFooter v-if="isLoggedIn()"
                :avatarUrl="authState.currentUser.avatarUrl"
                :name="authState.currentUser.name"
                info="abc@gmail.com"
                @click="handleLogout"
            />
        </div>
    </aside>
</template>

<script setup>
import logoURL from "@/assets/logo.svg";
import SidebarBtn from "./SidebarBtn.vue";
import SidebarFooter from "./SidebarFooter.vue";

import { useRouter } from "vue-router";
import { authState, logout, isLoggedIn } from '@/auth.js';

const router = useRouter();

function handleLogout() {
    logout(router);
}
</script>

<style lang="scss" scoped>
aside {
    display: flex;
    flex-direction: column;
    padding: 12px;
    height: 100svh;
    min-width: 200px;

    .logo {
        display: flex;
        margin: 16px auto 24px;
        gap: 1rem;

        img {
            width: 1.875rem;
        }

        p {
            font-size: 1.5625rem;
            font-weight: 700;
        }
    }

    .menu {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    .flex {
        flex: 1 1 0%;
    }
}

@media screen and (max-width: 1200px) {
    aside {
        min-width: fit-content;
    }

    .logo {
        p {
            display: none;
        }
    }
}

@media screen and (max-width: 1000px) {
    aside {
        display: none !important;
    }
}
</style>
