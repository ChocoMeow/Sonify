<template>
    <div :class="['track', { small: !isLarge }]">
        <div class="track-info">
            <AnimatedPlaceholder width="68px" height="68px" />
            <div class="detail">
                <AnimatedPlaceholder width="40%" height="20px" />
                <AnimatedPlaceholder width="60%" height="10px" />
                <div class="author">
                    <AnimatedPlaceholder
                        width="20px"
                        height="20px"
                        borderRadius="50%"
                    />
                    <AnimatedPlaceholder width="20%" height="10px" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import AnimatedPlaceholder from "./AnimatedPlaceholder.vue";

defineProps({
    isLarge: {
        type: Boolean,
        default: true,
    },
});
</script>

<style lang="scss" scoped>
.track {
    display: flex;
    justify-content: space-between;
    padding: 12px 20px;
    border-radius: 10px;
    gap: 20px;

    &.small {
        padding: 4px 8px;
    }

    .track-info {
        display: flex;
        align-items: center;
        gap: 20px;
        width: 100%;

        .detail {
            display: flex;
            flex-direction: column;
            width: 80%;
            gap: 7px;
        }

        .author {
            display: flex;
            align-items: center;
            gap: 10px;
        }
    }
}
</style>
