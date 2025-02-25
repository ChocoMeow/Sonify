<template>
    <div :class="['track', { small: !isLarge }]" @click="playTrack(track)">
        <div class="track-info">
            <p class="rank" v-if="rank">{{ rank }}</p>
            <img :src="track.thumbnail" alt="" />
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
defineProps({
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
            id: "1",
            title: "I Spent 3000 Credits on This Song",
            prompt: "jazz and trap slap guitar experimental flamenco math rock with layered harmonics",
            thumbnail:
                "https://cdn2.suno.ai/da064b7c-21c2-46e5-9689-55c52a57c2fd_2a504945.jpeg",
            duration: "3:15",
            likes: 0,
            author: {
                avatarUrl:
                    "https://cdn.discordapp.com/avatars/358819659581227011/5bb448ef85fc774d17d6b959903372f7.webp?size=1024",
                name: "Asher",
            },
        }),
    },
});

import { useAudioPlayer } from "@/composables/useAudioPlayer";

const { state, audioRef, addTrack, playTrackAtIndex } = useAudioPlayer();

const handleLinkClick = (event) => {
    event.preventDefault();
};

const playTrack = (track) => {
    const existingIndex = state.queue.findIndex((t) => t.src === track.src);

    if (existingIndex === -1) {
        addTrack(track);
        playTrackAtIndex(state.queue.length - 1);
    } else {
        playTrackAtIndex(existingIndex);
    }

    if (!state.isPlaying && audioRef.value) {
        const currentTrack = state.queue[state.currentIndex];

        audioRef.value.src = currentTrack.src;
        audioRef.value.load();

        audioRef.value.addEventListener(
            "canplaythrough",
            () => {
                state.isPlaying = true;
                audioRef.value.play();
            },
            { once: true }
        );
    }
};
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
</style>
