<template>
    <div class="not-found">
        <h1>404</h1>
        <h3>Oops! Page not found</h3>
        <p>The page you're looking for doesn't exist or has been moved.</p>

        <RoundedButton name="Go Back" @click="goBack" />
    </div>
</template>

<script setup>
import RoundedButton from "@/components/RoundedButton.vue";

import { useRouter } from "vue-router";

const router = useRouter();

function goBack() {
    router.go(-2);
}
</script>

<style lang="scss" scoped>
.not-found {
    height: 100svh;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    gap: 10px;

    h1 {
        font-size: 80px;
    }

    p {
        color: var(--sub-text);
        margin: 30px 0 20px;
    }
}
</style>
