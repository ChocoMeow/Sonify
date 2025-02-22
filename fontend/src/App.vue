<template>
    <div class="app">
        <Sidebar />
        <div class="content" ref="contentRef">
            <router-view :key="$route.fullPath"/>
        </div>
    </div>
</template>

<script setup>
import Sidebar from "@/components/sidebar/Sidebar.vue";
</script>

<style lang="scss">
a {
    color: var(--text);
    text-decoration: none;
}

.app {
    display: flex;
    width: 100vw;
    height: 100vh;

    .content {
        width: 80%;
        min-width: 700px;
        max-width: 1300px;
        margin: 0 auto;
        padding: 0 100px;
        overflow-y: auto;
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
}

::-webkit-scrollbar {
    width: 0px;
    height: 0px;
}

/* Track */
::-webkit-scrollbar-track {
    background: none;
}

/* Handle */
::-webkit-scrollbar-thumb {
    border-radius: 10px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
    background: var(--primary-200);
}
</style>
