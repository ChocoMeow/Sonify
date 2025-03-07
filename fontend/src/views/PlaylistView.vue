<template>
    <div class="playlist-view">
        <HeaderBar />
        <div v-if="playlist">
            <div class="playlist-info">
                <div class="track-imgs">
                    <img :src="playlist.tracks[0].thumbnail" alt="" />
                    <img :src="playlist.tracks[1].thumbnail" alt="" />
                    <img :src="playlist.tracks[2].thumbnail" alt="" />
                </div>
                <div class="info-section">
                    <div class="author">
                        <img :src="playlist.author.avatarUrl" alt="" />
                        <p class="clamp-text">{{ playlist.author.name }}</p>
                    </div>
                    <h3 class="clamp-text">{{ playlist.name }}</h3>
                    <p>{{ playlist.totalSongs }} Songs • 3h 43m</p>
                    <div class="action-btns">
                        <IconButton
                            icon="play_arrow"
                            backgroundColor="var(--text)"
                            textColor="var(--background)"
                            hoverColor="var(--sub-text)"
                        />
                        <IconButton icon="favorite" :isFill="false" />
                        <IconButton icon="share" :isFill="false" />
                    </div>
                </div>
            </div>
            <div class="tracks">
                <TrackRow
                    v-for="track in playlist.tracks"
                    :key="track"
                    :key="track.id"
                    :track="track"
                />
            </div>
        </div>
        <div v-else>
            <!-- Optionally, display a loading indicator -->
            Loading...
        </div>
    </div>
</template>

<script setup>
import HeaderBar from "@/components/HeaderBar.vue";
import IconButton from "@/components/IconButton.vue";
import TrackRow from "@/components/TrackRow.vue";

import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { apiFetch } from "@/auth.js";

const route = useRoute();
const router = useRouter();

const playlistId = route.params.id;
const playlist = ref(null);

onMounted(async () => {
    try {
        const data = await apiFetch(`${import.meta.env.VITE_API_URL}playlist`, {
            method: "POST",
            body: JSON.stringify({ playlist_id: playlistId }),
        });
        playlist.value = data;
    } catch (error) {
        console.error("Error fetching track:", error);
        router.push({ name: "page-not-found", query: { backTo: -2 } });
    }
});
</script>

<style lang="scss" scoped>
.playlist-info {
    display: flex;
    padding: 20px;
    gap: 20px;
    border-radius: 10px;
    align-items: center;
    white-space: nowrap;
    background-color: var(--primary-100);

    .track-imgs {
        position: relative;
        min-width: 205px;
        height: 180px;

        img {
            position: absolute;
            width: 120px;
            height: 120px;
            border-radius: 10px;
            box-shadow: var(--background) -4px 9px 25px -6px;
            object-fit: cover;

            &:nth-child(1) {
                transform: translate(45px, 5px);
            }
            &:nth-child(2) {
                transform: rotate(-9.95deg) translate(5px, 20px);
                z-index: -2;
            }

            &:nth-child(3) {
                transform: rotate(13.23deg) translate(85px, 28px);
                z-index: -1;
            }
        }
    }
}

.info-section {
    display: flex;
    flex-direction: column;
    gap: 4px;
    flex-grow: 1;
    padding: 0 5px;
    overflow: hidden;

    p {
        color: var(--sub-text);
    }

    .author {
        display: flex;
        align-items: center;
        gap: 10px;

        img {
            width: 22px;
            height: 22px;
            border-radius: 50%;
        }
    }

    .action-btns {
        margin-top: 15px;
        display: flex;
        gap: 8px;
    }
}

.tracks {
    padding: 20px 0;
}
</style>
