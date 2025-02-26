<template>
    <div class="footer">
        <img :src="avatarUrl ? avatarUrl : defaultAvatarUrl" alt="" />
        <div class="user-info">
            <p class="clamp-text">{{ name }}</p>
        </div>
        <div class="flex"></div>
        <span v-if="isLoggedIn()" class="material-symbols-rounded" style="color: var(--error)"> logout </span>
    </div>
</template>

<script setup>
import { isLoggedIn } from "@/auth.js";

import defaultAvatarUrl from "@/assets/avatar.jpg";

defineProps({
    avatarUrl: {
        type: String,
        default: "",
    },
    name: {
        type: String,
        default: "",
    }
});
</script>

<style lang="scss" scoped>
.footer {
    display: flex;
    gap: 12px;
    width: 100%;
    align-items: center;
    padding: 12px 20px;
    border-radius: 50px;
    cursor: pointer;
    background-color: var(--primary-100);

    img {
        width: 32px;
        height: 32px;
        border-radius: 50%;
    }

    .flex {
        flex: 1 1 0%;
    }
}

@media screen and (max-width: 1200px) {
    .user-info,
    .flex,
    span {
        display: none;
    }

    img {
        width: 24px !important;
        height: 24px !important;
    }
}
</style>
