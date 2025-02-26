<template>
    <div class="playlist-cards">
        <div class="playlist-card">
            <div class="playlist-card__content">
                <!-- Skeleton for title -->
                <AnimatedPlaceholder width="120px" height="20px" />

                <!-- Skeleton for prompt -->
                <AnimatedPlaceholder width="180px" height="10px" />
                <AnimatedPlaceholder width="150px" height="10px" />

                <!-- Skeleton for songs count -->
                <AnimatedPlaceholder width="80px" height="15px" />

                <!-- Skeleton for footer -->
                <div class="playlist-card__footer">
                    <AnimatedPlaceholder width="24px" height="24px" borderRadius="50%"/>
                    <AnimatedPlaceholder width="60px" height="16px" />
                </div>
            </div>
            <div class="playlist-card__image-container">
                <AnimatedPlaceholder width="200px" height="100%" />
            </div>
        </div>
    </div>
</template>

<script setup>
import AnimatedPlaceholder from "./AnimatedPlaceholder.vue";
</script>

<style lang="scss" scoped>
.playlist-cards {
    min-width: 200px;
    height: 300px;
    position: relative;
}

.playlist-card {
    height: 300px;
    position: absolute;
    border-radius: 8px;
    overflow: hidden;
    transition: all 0.4s;
    z-index: 0;
    box-shadow: rgb(0, 0, 0) 0px -3px 10px 0px;

    &__content {
        display: flex;
        flex-direction: column;
        position: absolute;
        padding: 12px;
        bottom: 0;
        gap: 8px;
        width: 100%;
    }

    &__footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    &__author {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    &__image-container {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: -1;
    }
}
</style>
