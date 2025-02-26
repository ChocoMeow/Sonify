<template>
    <div class="search-view">
        <HeaderBar />

        <Tabs>
            <Tab name="All">
                <div class="sections">
                    <div class="section">
                        <div class="header">
                            <h2>Songs</h2>
                        </div>
                        <div class="tracks">
                            <template v-if="tracks && tracks.length > 0">
                                <TrackRow
                                    v-for="track in tracks"
                                    :key="track.id"
                                    :track="track"
                                />
                            </template>
                            <template v-else-if="trackMessage">
                                <p>{{ trackMessage }}</p>
                            </template>
                            <template v-else>
                                <TrackRowSkeleton v-for="n in 6" :key="n" />
                            </template>
                        </div>
                    </div>

                    <div class="section">
                        <div class="header">
                            <h2>Playlists</h2>
                        </div>
                        <template v-if="playlists && playlists.length > 0">
                            <div class="playlists">
                                <PlaylistCard
                                    v-for="playlist in playlists"
                                    :key="playlist.id"
                                    :playlist="playlist"
                                    style="padding: 26px 0"
                                />
                            </div>
                        </template>
                        <template v-else-if="playlistMessage">
                            <p>{{ playlistMessage }}</p>
                        </template>
                        <template v-else>
                            <div class="playlists">
                                <PlaylistCardSkeleton v-for="n in 6" :key="n" />
                            </div>
                        </template>
                    </div>
                </div>
            </Tab>
            <Tab name="Songs">
                <div class="sections">
                    <div class="section">
                        <div class="header">
                            <h2>Songs</h2>
                        </div>
                        <div class="tracks">
                            <template v-if="tracks && tracks.length > 0">
                                <TrackRow
                                    v-for="track in tracks"
                                    :key="track.id"
                                    :track="track"
                                />
                            </template>
                            <template v-else-if="trackMessage">
                                <p>{{ trackMessage }}</p>
                            </template>
                            <template v-else>
                                <TrackRowSkeleton v-for="n in 6" :key="n" />
                            </template>
                        </div>
                    </div>
                </div>
            </Tab>
            <Tab name="Playlists">
                <div class="sections">
                    <div class="section">
                        <div class="header">
                            <h2>Playlists</h2>
                        </div>
                        <template v-if="playlists && playlists.length > 0">
                            <div class="playlists">
                                <PlaylistCard
                                    v-for="playlist in playlists"
                                    :key="playlist.id"
                                    :playlist="playlist"
                                    style="padding: 26px 0"
                                />
                            </div>
                        </template>
                        <template v-else-if="playlistMessage">
                            <p>{{ playlistMessage }}</p>
                        </template>
                        <template v-else>
                            <div class="playlists">
                                <PlaylistCardSkeleton v-for="n in 6" :key="n" />
                            </div>
                        </template>
                    </div>
                </div>
            </Tab>
        </Tabs>
    </div>
</template>

<script setup>
import HeaderBar from "@/components/HeaderBar.vue";
import Tabs from "@/components/tab/Tabs.vue";
import Tab from "@/components/tab/Tab.vue";

import TrackRow from "@/components/TrackRow.vue";
import TrackRowSkeleton from "@/components/skeleton/TrackRowSkeleton.vue";
import PlaylistCard from "@/components/PlaylistCard.vue";
import PlaylistCardSkeleton from "@/components/skeleton/PlaylistCardSkeleton.vue";

import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { apiFetch } from "@/auth.js";

const route = useRoute();

const tracks = ref(null);
const playlists = ref(null);

const trackMessage = ref("");
const playlistMessage = ref("");

onMounted(async () => {
    try {
        const searchQuery = route.query.search_query || "";
        const data = await apiFetch(`${import.meta.env.VITE_API_URL}search`, {
            method: "POST",
            body: JSON.stringify({ search_query: searchQuery }),
        });
        tracks.value = data.tracks || [];
        playlists.value = data.playlists || [];
        if (!tracks.value.length) {
            trackMessage.value = "No results found.";
        }

        if (!playlists.value.length) {
            playlistMessage.value = "No results found.";
        }
    } catch (error) {
        trackMessage.value = "Error loading search data";
        playlistMessage.value = "Error loading search data";
        console.error(error);
    }
});
</script>

<style lang="scss" scoped>
.sections {
    display: flex;
    flex-direction: column;
    gap: 20px;

    .header {
        padding-bottom: 10px;
    }

    .playlists {
        display: grid;
        row-gap: 40px;
        grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
    }
}
</style>
