<template>
    <div :class="['track', { small: !isLarge }]" @click="toggleTrack(track)">
        <div class="track-info">
            <p class="rank" v-if="rank">{{ rank }}</p>
            <div class="image-container">
                <img :src="track.thumbnail" alt="" />
                <div class="waves" v-if="isThisTrackPlaying">
                    <div class="wave" v-for="n in 3" :key="n"></div>
                </div>
            </div>
            <div class="detail">
                <router-link
                    :to="{ name: 'track', params: { id: track.id } }"
                    @click.stop="handleLinkClick"
                >
                    <h3 class="track-title clamp-text">{{ track.title }}</h3>
                </router-link>
                <p class="clamp-text">{{ track.prompt }}</p>
                <div class="author">
                    <img :src="track.author.avatarUrl" alt="" />
                    <p>{{ track.author.name }}</p>
                </div>
            </div>
        </div>
        <div class="right">
            <div class="likes" v-if="isLarge">
                <span class="material-symbols-rounded"> thumb_up </span>
                <p>{{ track.likes }}</p>
            </div>
            <p>{{ track.duration }}</p>
            <span class="material-symbols-rounded action" v-if="isLarge">
                favorite
            </span>
            <span class="material-symbols-rounded action" v-if="isLarge">
                more_horiz
            </span>
        </div>
    </div>
</template>

<script setup>
import { computed } from "vue";
import { useAudioPlayer } from "@/composables/useAudioPlayer";

const props = defineProps({
    rank: {
        type: String,
        default: "",
    },
    isLarge: {
        type: Boolean,
        default: true,
    },
    track: {
        type: Object,
        default: () => ({
            id: "",
            title: "",
            prompt: "",
            thumbnail: "",
            duration: "",
            likes: 0,
            author: {
                avatarUrl: "",
                name: "",
            },
        }),
    },
});

const { state, audioRef, playTrack, currentTrack } = useAudioPlayer();

const isThisTrackPlaying = computed(() => {
    return (
        state.isPlaying &&
        state.queue[state.currentIndex]?.id === props.track?.id
    );
});

const handleLinkClick = (event) => {
    event.preventDefault();
};

const toggleTrack = (track) => {
    if (currentTrack.value?.id === track.id) {
        const isPlaying = state.isPlaying;
        isPlaying ? audioRef.value.pause() : audioRef.value.play();
        state.isPlaying = !isPlaying;
    } else {
        playTrack(track);
    }
}
</script>

<style lang="scss" scoped>
.track {
    display: flex;
    justify-content: space-between;
    padding: 12px 20px;
    border-radius: 10px;
    transition: background-color 0.1s;
    gap: 20px;
    cursor: pointer;

    &:hover {
        background-color: var(--primary-200);
    }

    &.small {
        padding: 4px 8px;
    }

    .track-info {
        display: flex;
        align-items: center;
        gap: 20px;
        width: 100%;

        .image-container {
            position: relative;
            min-width: 68px;
            height: 68px;
            border-radius: 10px;
            overflow: hidden;
        }

        img {
            width: 68px;
            height: 68px;
            border-radius: 10px;
        }

        .rank {
            font-size: 25px;
            font-weight: 700;
            color: var(--sub-text);
            letter-spacing: 2px;
        }

        .detail {
            display: flex;
            flex-direction: column;

            p {
                font-size: 12px;
                color: var(--sub-text);
            }

            .track-title {
                &:hover {
                    text-decoration: underline;
                }
            }
        }

        .author {
            display: flex;
            align-items: center;
            margin: 5px 0;
            gap: 10px;

            img {
                width: 20px;
                height: 20px;
            }
        }
    }

    .right {
        display: flex;
        align-items: center;
        gap: 25px;

        .likes {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .action {
            transition: scale 0.1s;
            &:hover {
                scale: 1.1;
            }
            &:active {
                scale: 0.9;
            }
        }
    }
}

.waves {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5px;
    background-color: var(--background-500);
    --_m: 10;

    .wave {
        aspect-ratio: 0.185/1;
        background-color: var(--text);
        border-radius: 15px;
        width: 5px;

        &:nth-child(1) {
            animation: waveform calc(200ms * var(--_m)) ease-in-out infinite
                forwards;
        }
        &:nth-child(2) {
            animation: waveform calc(100ms * var(--_m)) ease-in-out infinite
                forwards;
        }
        &:nth-child(3) {
            animation: waveform calc(500ms * var(--_m)) ease-in-out infinite
                forwards;
        }
    }
}

@keyframes waveform {
    0% {
        transform: scaleY(0.4);
    }
    50% {
        transform: scaleY(1);
    }
    100% {
        transform: scaleY(0.4);
    }
}
</style>
