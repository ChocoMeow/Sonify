<template>
    <div class="textbox-skeleton">
        <AnimatedPlaceholder
            v-for="(width, index) in randomWidths"
            :key="index"
            :width="width"
            height="18px"
        />
    </div>
</template>

<script setup>
import AnimatedPlaceholder from "./AnimatedPlaceholder.vue";

const props = defineProps({
    length: {
        type: Number,
        default: 10,
    },
});

const randomWidths = Array.from({ length: props.length }, () => {
    const randomWidth = Math.floor(Math.random() * (80 - 30 + 1)) + 30;
    return `${randomWidth}%`;
});
</script>

<style>
.textbox-skeleton {
    display: flex;
    flex-direction: column;
    gap: 15px;
    width: 100%;
}
</style>
