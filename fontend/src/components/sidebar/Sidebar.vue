<template>
    <aside>
        <router-link to="/" class="logo">
            <img :src="logoURL" alt="" />
            <p>Sonify</p>
        </router-link>

        <div class="menu">
            <SidebarBtn path="/" icon="home" name="Home" />
            <SidebarBtn path="/create" icon="music_note_add" name="Create" />
            <SidebarBtn path="/library" icon="bookmarks" name="Library" />
        </div>

        <div class="flex"></div>

        <div class="menu">
            <SidebarBtn path="/support" icon="help" name="Support" />
            <SidebarFooter
                avatarUrl="https://cdn.discordapp.com/avatars/358819659581227011/5bb448ef85fc774d17d6b959903372f7.webp?size=1024"
                name="Asher"
                info="abc@gmail.com"
            />
        </div>
    </aside>
</template>

<script setup>
import logoURL from "@/assets/logo.svg";
import SidebarBtn from "./SidebarBtn.vue";
import SidebarFooter from "./SidebarFooter.vue";
</script>

<style lang="scss" scoped>
aside {
    display: flex;
    flex-direction: column;
    padding: 12px;
    height: 100svh;
    width: fit-content;

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
