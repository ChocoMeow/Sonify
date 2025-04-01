<template>
    <div class="track-view">
        <HeaderBar />
        <div v-if="track">
            <div class="wrapper">
                <div class="track-content">
                    <div class="track-info">
                        <img :src="track?.thumbnail" alt="" />

                        <div class="info-section">
                            <div class="author">
                                <img :src="track.author.avatarUrl" alt="" />
                                <p class="clamp-text">
                                    {{ track.author.name }}
                                </p>
                            </div>

                            <h3 class="clamp-text">{{ track.title }}</h3>
                            <p>{{ track.prompt }}</p>

                            <div class="action-btns">
                                <IconButton
                                    icon="pause"
                                    v-if="
                                        currentTrack?.id === track.id &&
                                        state.isPlaying
                                    "
                                    @click="pause"
                                    backgroundColor="var(--text)"
                                    textColor="var(--background)"
                                    hoverColor="var(--sub-text)"
                                />
                                <IconButton
                                    icon="play_arrow"
                                    v-else
                                    @click="toggleTrack(track)"
                                    backgroundColor="var(--text)"
                                    textColor="var(--background)"
                                    hoverColor="var(--sub-text)"
                                />
                                <IconButton icon="favorite" :isFill="false" />
                                <IconButton icon="share" :isFill="false" />
                            </div>
                        </div>
                    </div>

                    <h2>Lyrics</h2>
                    <p class="lyrics-text">{{ track.lyrics }}</p>
                </div>
                <div class="right">
                    <Tabs>
                        <Tab name="Similar" class="tracks">
                            <template v-if="similarTracks">
                                <TrackRow
                                    :isLarge="false"
                                    v-for="track in similarTracks"
                                    :key="track.id"
                                    :track="track"
                                />
                            </template>
                            <template v-else>
                                <TrackRowSkeleton
                                    v-for="n in 7"
                                    :key="n"
                                    :isLarge="false"
                                />
                            </template>
                        </Tab>
                        <Tab
                            :name="'By ' + track.author.name"
                            :asyncFunction="requestAuthorTrack"
                            class="tracks"
                        >
                            <template v-if="authorTracks">
                                <TrackRow
                                    :isLarge="false"
                                    v-for="track in authorTracks"
                                    :key="track.id"
                                    :track="track"
                                />
                            </template>
                            <template v-else>
                                <TrackRowSkeleton
                                    v-for="n in 7"
                                    :key="n"
                                    :isLarge="false"
                                />
                            </template>
                        </Tab>
                    </Tabs>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import HeaderBar from "@/components/HeaderBar.vue";
import IconButton from "@/components/IconButton.vue";
import Tabs from "@/components/tab/Tabs.vue";
import Tab from "@/components/tab/Tab.vue";
import TrackRow from "@/components/TrackRow.vue";
import TrackRowSkeleton from "@/components/skeleton/TrackRowSkeleton.vue";

import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";

import { useAudioPlayer } from "@/composables/useAudioPlayer";
import { apiFetch } from "@/auth.js";

const { state, currentTrack, audioRef, playTrack } = useAudioPlayer();

const route = useRoute();
const router = useRouter();

const trackId = route.params.id;

const track = ref(null);
const similarTracks = ref(null);
const authorTracks = ref(null);

onMounted(async () => {
    try {
        const data = await apiFetch(`${import.meta.env.VITE_API_URL}track`, {
            method: "POST",
            body: JSON.stringify({ track_id: trackId }),
        });
        track.value = data;
    } catch (error) {
        console.error("Error fetching track:", error);
        router.push({ name: "page-not-found", query: { backTo: -2 } });
    }

    try {
        const data = await apiFetch(`${import.meta.env.VITE_API_URL}similar`, {
            method: "POST",
            body: JSON.stringify({ track_id: trackId }),
        });
        similarTracks.value = data.tracks;
    } catch (error) {
        console.error("Error fetching track:", error);
    }
});

const requestAuthorTrack = async () => {
    try {
        if (!track || authorTracks.value) {
            return;
        }
        const data = await apiFetch(
            `${import.meta.env.VITE_API_URL}userTracks`,
            {
                method: "POST",
                body: JSON.stringify({ user_id: track.value.author.id }),
            }
        );
        authorTracks.value = data.tracks;
    } catch (error) {
        console.error("Error fetching track:", error);
    }
};

const toggleTrack = (track) => {
    if (currentTrack.value?.id === track.id) {
        const isPlaying = state.isPlaying;
        isPlaying ? audioRef.value.pause() : audioRef.value.play();
        state.isPlaying = !isPlaying;
    } else {
        playTrack(track);
    }
};

const pause = () => {
    if (audioRef.value) {
        audioRef.value.pause();
        state.isPlaying = false;
    }
};
</script>

<style lang="scss" scoped>
.wrapper {
    display: flex;
    gap: 20px;

    .right {
        width: 40%;
    }
}

.track-content {
    width: 60%;
    padding-bottom: 100px;

    h2 {
        padding: 20px 0 10px;
    }

    .lyrics-text {
        white-space: pre-wrap;
    }
}

.tracks {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 100%;
}
.track-info {
    display: flex;
    padding: 20px;
    gap: 20px;
    border-radius: 10px;
    align-items: center;
    white-space: nowrap;
    background-color: var(--primary-100);

    img {
        width: 160px;
        height: 160px;
        object-fit: cover;
        border-radius: 10px;
    }

    .info-section {
        display: flex;
        flex-direction: column;
        gap: 4px;
        padding: 0 5px;
        overflow: hidden;

        p {
            color: var(--sub-text);
            font-size: 14px;
        }

        .author {
            display: flex;
            align-items: center;
            margin-bottom: 5px;
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
}

@media screen and (max-width: 1000px) {
    .wrapper {
        flex-direction: column;

        .right {
            width: 100%;
        }
    }

    .track-content {
        width: 100%;
        padding-bottom: 20px;
    }
}
</style>
