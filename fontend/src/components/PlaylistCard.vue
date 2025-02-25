<template>
    <router-link :to="{ name: 'playlist', params: { id: playlist.id } }">
        <div class="playlist-cards">
            <div class="playlist-card" v-if="mainTrack">
                <div class="playlist-card__content">
                    <div class="playlist-card__type">
                        <p>{{ playlist.type }}</p>
                    </div>
                    <h4 class="clamp-text">{{ playlist.name }}</h4>
                    <p class="playlist-card__prompt clamp-text line2">
                        {{ mainTrack.prompt }}
                    </p>
                    <p>{{ playlist.totalSongs }} Songs</p>
                    <div class="playlist-card__footer">
                        <div class="playlist-card__author">
                            <img
                                :src="playlist.author.avatarUrl"
                                :alt="`Avatar of ${playlist.author.name}`"
                            />
                            <p>{{ playlist.author.name }}</p>
                        </div>
                        <div class="playlist-card__likes">
                            <p>{{ playlist.likes }}</p>
                            <span class="material-symbols-rounded fill"
                                >thumb_up</span
                            >
                        </div>
                    </div>
                </div>
                <div class="playlist-card__image-container">
                    <img
                        :src="mainTrack.thumbnail"
                        :alt="`Thumbnail for ${mainTrack.title}`"
                    />
                    <div class="playlist-card__overlay"></div>
                </div>
            </div>
            <img
                v-if="thirdTrack"
                class="playlist-card__background-image--tertiary"
                :src="thirdTrack.thumbnail"
                :alt="`Thumbnail for ${thirdTrack.title}`"
            />
            <img
                v-if="secondTrack"
                class="playlist-card__background-image--secondary"
                :src="secondTrack.thumbnail"
                :alt="`Thumbnail for ${secondTrack.title}`"
            />
        </div>
    </router-link>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
    playlist: {
        type: Object,
        default: () => ({
            tracks: [
                {
                    title: "Forgiveness",
                    prompt: "Neo-Soul, Contemporary R&B, Soul, Soul, Pop, Jazz",
                    thumbnail:
                        "https://cdn2.suno.ai/77452488-4087-4e2c-855c-f59246145278_4f1ee7f5.jpeg",
                },
                {
                    title: "Unknown 2",
                    prompt: "Unknown prompt",
                    thumbnail:
                        "https://cdn2.suno.ai/13119adb-533b-4830-bce2-dfedada73552_1386cf35.jpeg",
                },
                {
                    title: "Unknown 3",
                    prompt: "Unknown prompt",
                    thumbnail:
                        "https://cdn2.suno.ai/image_large_0f1aeee9-3764-437b-ae54-21175b3374ae.jpeg",
                },
            ],
            totalSOngs: 0,
            author: {
                avatarUrl:
                    "https://cdn.discordapp.com/avatars/358819659581227011/5bb448ef85fc774d17d6b959903372f7.webp?size=1024",
                name: "Asher",
            },
            likes: 0,
            type: "Playlist",
        }),
    },
});

// Destructure tracks using computed properties
const mainTrack = computed(() => props.playlist?.tracks?.[0]);
const secondTrack = computed(() => props.playlist?.tracks?.[1]);
const thirdTrack = computed(() => props.playlist?.tracks?.[2]);
</script>

<style lang="scss" scoped>
.playlist-cards {
    width: 200px;
    height: 300px;
    position: relative;

    &:hover {
        .playlist-card {
            transform: translateY(-14px);
        }
        .playlist-card__background-image--secondary {
            width: 85%;
            transform: translate(-50%, -8px);
        }
        .playlist-card__background-image--tertiary {
            width: 75%;
        }
    }

    .playlist-card__background-image--secondary {
        position: absolute;
        top: -14px;
        width: 90%;
        margin: 0 auto;
        z-index: -1;
        border-radius: 8px;
        left: 50%;
        transform: translate(-50%, 0);
        transition: all 0.3s;
    }

    .playlist-card__background-image--tertiary {
        position: absolute;
        top: -24px;
        width: 80%;
        z-index: -2;
        border-radius: 8px;
        left: 50%;
        transform: translate(-50%, 0);
        transition: all 0.2s;
    }
}

.playlist-card {
    height: 300px;
    position: absolute;
    border-radius: 8px;
    overflow: hidden;
    transition: all 0.4s;
    z-index: 0;
    box-shadow: rgb(0, 0, 0) 0px -3px 10px 0px;
    cursor: pointer;

    p {
        font-size: 12px;
    }

    &__content {
        display: flex;
        flex-direction: column;
        position: absolute;
        padding: 12px;
        bottom: 0;
        gap: 6px;
        width: 100%;
    }

    &__type {
        width: min-content;
        padding: 4px 16px;
        border-radius: 20px;
        background-color: var(--primary-700);
    }

    &__prompt {
        color: var(--sub-text);
        font-size: 10px;
        min-height: 36px;
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

        img {
            width: 24px;
            border-radius: 50%;
        }
    }

    &__likes {
        display: flex;
        align-items: center;
        gap: 8px;

        .material-symbols-rounded {
            font-size: 16px;
        }
    }

    &__image-container {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: -1;

        img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            will-change: transform;
            transform: translate3d(0, 0, 0);
            backface-visibility: hidden;
        }
    }

    &__overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            to bottom,
            rgba(255, 255, 255, 0) 0%,
            rgba(0, 0, 0, 0.7) 100%
        );
        pointer-events: none;
    }
}
</style>
