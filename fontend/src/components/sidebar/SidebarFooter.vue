<template>
    <div class="footer">
        <img :src="avatarUrl" alt="" />
        <div class="user-info">
            <p>{{ name }}</p>
        </div>
        <div class="flex"></div>
        <span class="material-symbols-rounded" style="color: var(--error)"> logout </span>
    </div>
</template>

<script setup>
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
</style>
