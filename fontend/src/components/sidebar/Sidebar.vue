<template>
    <aside>
        <router-link :to="{ name: 'home' }" class="logo">
            <img :src="logoURL" alt="" />
            <p>Sonify</p>
        </router-link>

        <div class="menu">
            <SidebarBtn icon="home" name="Home" routeName="home" />
            <SidebarBtn icon="music_note_add" name="Create" routeName="create" />
            <SidebarBtn icon="bookmarks" name="Library" routeName="library" />
        </div>

        <div class="flex"></div>

        <div class="menu">
            <SidebarBtn 
                icon="fa-circle-info" 
                iconType="fa-solid" 
                name="Support" 
                href="https://github.com/ChocoMeow/Sonify" 
                newTab="true" 
            />
            <SidebarBtn 
                icon="fa-github" 
                iconType="fa-brands"
                name="Github" 
                href="https://github.com/ChocoMeow/Sonify" 
                newTab="true" 
            />
            
            <template v-if="isLoggedIn()">
                <SidebarFooter
                    :avatarUrl="authState.currentUser.avatarUrl"
                    :name="authState.currentUser.name"
                    :info="authState.currentUser.email"
                    @click="handleLogout"
                />
            </template>
            <template v-else>
                <SidebarFooter :avatarUrl="defaultIconUrl" name="Sign In" @click="handleLogin" />
            </template>
        </div>
    </aside>
</template>

<script setup>
import logoURL from "@/assets/logo.svg";
import defaultIconUrl from "@/assets/avatar.jpg";
import SidebarBtn from "./SidebarBtn.vue";
import SidebarFooter from "./SidebarFooter.vue";

import { useRouter } from "vue-router";
import { authState, logout, isLoggedIn } from "@/auth.js";

const router = useRouter();

function handleLogout() {
    logout(router);
}

function handleLogin() {
    router.push({ name: "login" });
}
</script>

<style lang="scss" scoped>
aside {
    display: flex;
    flex-direction: column;
    padding: 12px;
    height: 100svh;
    min-width: 210px;

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
