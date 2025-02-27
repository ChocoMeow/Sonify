<template class="app">
    <div>
        <HeaderBar />
        <div class="section">
            <div class="header">
                <h2>Featured Playlists</h2>
                <p>Show More ></p>
            </div>
            <div ref="containerRef" class="scroll-container">
                <template v-if="playlists">
                    <PlaylistCard
                        v-for="playlist in playlists"
                        :key="playlist"
                        :playlist="playlist"
                    />
                </template>
                <template v-else>
                    <PlaylistCardSkeleton v-for="n in 10" :key="n" />
                </template>
            </div>
        </div>

        <div class="section">
            <div class="header">
                <h2>Global Trending</h2>
                <p>Show More ></p>
            </div>
        </div>

        <template v-if="tracks">
            <TrackRow
                v-for="(track, index) in tracks"
                :key="index"
                :rank="String(index + 1).padStart(2, '0')"
                :track="track"
            />
        </template>
        <template v-else>
            <TrackRowSkeleton v-for="n in 10" :key="n" />
        </template>
    </div>
</template>

<script setup>
import HeaderBar from "@/components/HeaderBar.vue";
import PlaylistCard from "@/components/PlaylistCard.vue";
import TrackRow from "@/components/TrackRow.vue";
import TrackRowSkeleton from "@/components/skeleton/TrackRowSkeleton.vue";
import PlaylistCardSkeleton from "@/components/skeleton/PlaylistCardSkeleton.vue";

import { onMounted, onUnmounted, ref } from "vue";

const containerRef = ref(null);

const updateMask = () => {
    const container = containerRef.value;
    if (!container) return;

    const scrollLeft = container.scrollLeft;
    const scrollWidth = container.scrollWidth;
    const clientWidth = container.clientWidth;

    let mask =
        "linear-gradient(to right, transparent, black 10%, black 90%, transparent)";

    if (scrollLeft <= 0) {
        mask = "linear-gradient(to right, black, black 90%, transparent)"; // No fade on the left
    }
    if (scrollLeft + clientWidth >= scrollWidth) {
        mask = "linear-gradient(to right, transparent, black 10%, black)"; // No fade on the right
    }
    if (scrollLeft <= 0 && scrollLeft + clientWidth >= scrollWidth) {
        mask = "none"; // No fade if no overflow
    }

    container.style.maskImage = mask;
    container.style.webkitMaskImage = mask;
};

onMounted(() => {
    if (containerRef.value) {
        containerRef.value.addEventListener("scroll", updateMask);
        updateMask();
    }
});

onUnmounted(() => {
    if (containerRef.value) {
        containerRef.value.removeEventListener("scroll", updateMask);
    }
});

const playlists = ref(null);
const tracks = ref(null);

const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json" },
};

fetch(`${import.meta.env.VITE_API_URL}popular`, requestOptions)
    .then((response) => response.json())
    .then((data) => {
        playlists.value = data.playlists;
        tracks.value = data.tracks;
    })
    .catch((error) => {
        console.error("Error fetching track:", error);
    });
</script>

<style lang="scss" scoped>
.btn {
    display: flex;
    height: 48px;
    justify-content: center;
    align-content: center;
    padding: 12px 20px;
    background-color: var(--accent);
    border-radius: 1rem;
    gap: 12px;
    cursor: pointer;
    transition: background-color 0.2s;

    &:hover {
        background-color: var(--secondary);
    }
}

.section {
    overflow: hidden;
    margin-top: 10px;

    .header {
        display: flex;
        justify-content: space-between;
        padding: 10px 0;
        align-items: end;
        z-index: 0;

        p {
            cursor: pointer;

            &:hover {
                text-decoration: underline;
            }
        }
    }

    .scroll-container {
        display: flex;
        margin: 20px 0 0;
        padding: 26px 0;
        gap: 20px;
        overflow-x: scroll;
        scrollbar-width: none;
        transition: mask-image 0.3s ease-out, -webkit-mask-image 0.3s ease-out;
    }
}
</style>
