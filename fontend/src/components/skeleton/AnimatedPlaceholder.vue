<template>
    <div class="placeholder">&nbsp;</div>
</template>

<script setup>
defineProps({
    height: {
        type: String,
    },
    width: {
        type: String,
    },
    borderRadius: {
        type: String,
        default: "10px"
    },
});
</script>

<style scoped>
@keyframes bgAnimate {
    0% {
        background-position: 50% 0;
    }

    100% {
        background-position: -150% 0;
    }
}
.placeholder {
    height: v-bind(height);
    width: v-bind(width);
    border-radius: v-bind(borderRadius);
    background-image: linear-gradient(
        to right,
        var(--primary-100) 0%,
        var(--primary-100) 10%,
        var(--primary-200) 20%,
        var(--primary-100) 100%
    );
    background-size: 200% 100%;
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    animation: bgAnimate 2s linear infinite;
}
</style>
