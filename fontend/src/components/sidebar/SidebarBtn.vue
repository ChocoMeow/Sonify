<template>
    <router-link :to="path" class="btn" :title="name">
        <span class="material-symbols-rounded fill">{{ icon }}</span>
        <p>{{ name }}</p>
    </router-link>
</template>

<script setup>
defineProps({
    path: {
        type: String,
        default: "/",
    },
    icon: {
        type: String,
        default: "home",
    },
    name: {
        type: String,
        default: "Home",
    },
});
</script>

<style lang="scss" scoped>
.btn {
    display: flex;
    gap: 12px;
    width: 100%;
    align-items: center;
    padding: 12px 20px;
    border-radius: 50px;
    cursor: pointer;

    &:hover {
        background-color: var(--primary-200);
    }

    &.router-link-exact-active {
        background-color: var(--primary-100);
        color: var(--primary);
    }

    p {
        overflow: hidden;
        text-overflow: ellipsis;
    }
}

@media screen and (max-width: 1200px) {
    .btn {
        width: fit-content;
        p {
            display: none;
        }
    }
}
</style>
