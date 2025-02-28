<template>
    <div class="app">
        <Sidebar v-if="!$route.meta.hideSidebar" />
        <div class="main-content">
            <div class="content-wrapper">
                <div class="main-scroll-container">
                    <div class="content">
                        <router-view :key="$route.fullPath" />
                    </div>
                </div>
                <MusicController v-if="!$route.meta.hideSidebar" />
            </div>
        </div>
    </div>
</template>

<script setup>
import Sidebar from "@/components/sidebar/Sidebar.vue";
import MusicController from "@/components/MusicController.vue";
</script>

<style lang="scss">
a {
    color: var(--text);
    text-decoration: none;
}

.app {
    display: flex;
    width: 100vw;
    height: 100svh;
}

.main-content {
    width: 100%;
    height: 100%;
    overflow-y: auto;
}

.content-wrapper {
    width: 80%;
    max-width: 1320px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    min-height: 100%;
}

.main-scroll-container {
    flex-grow: 1;
    overflow-y: auto;
}

.content {
    position: relative;
    flex-grow: 1;
    padding: 0 5px;
}

.clamp-text {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    overflow: hidden;
    -webkit-line-clamp: 1;

    &.line2 {
        -webkit-line-clamp: 2;
    }
}

.material-symbols-rounded.fill {
    font-variation-settings: "FILL" 1;
}

::-webkit-scrollbar {
    width: 10px;
    height: 10px;
    background: none;
}

/* Track */
::-webkit-scrollbar-track {
    background: none;
}

/* Handle */
::-webkit-scrollbar-thumb {
    border-radius: 10px;
    cursor: pointer;
    background-color: var(--background-2);
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
    background: var(--primary-200);
}

@media screen and (max-width: 800px) {
    .content-wrapper {
        width: 100% !important;
        padding: 0 20px !important;
    }
}
</style>
