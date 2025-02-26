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

                    <h2>Lyrics</h2>
                    <p class="lyrics-text">{{ track.lyrics }}</p>
                </div>
                <div class="right">
                    <Tabs>
                        <Tab name="Similar" class="tracks">
                            <template v-if="similarTrack">
                                <TrackRow
                                    :isLarge="false"
                                    v-for="track in similarTrack"
                                    :key="track"
                                    :track="track"
                                />
                            </template>
                            <template v-else>
                                <TrackRowSkeleton v-for="n in 10" :key="n" :isLarge="false"/>
                            </template>
                        </Tab>
                        <Tab :name="'By ' + track.author.name" />
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

import { ref } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const trackId = route.params.id;

defineProps({
    track: {
        type: Object,
        default: () => ({
            id: "",
            title: "Unknown",
            duration: "00:00",
            prompt: "Unknown",
            thumbnail: "",
            lyrics: "",
            author: {
                avatarUrl: "",
                name: "Unknown",
            },
        }),
    },
});

const track = ref(null);
const similarTrack = ref(null);

fetch(`${import.meta.env.VITE_API_URL}track`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ track_id: trackId }),
})
    .then((response) => response.json())
    .then((data) => {
        track.value = data;
    })
    .catch((error) => {
        console.error("Error fetching track:", error);
    });

fetch(`${import.meta.env.VITE_API_URL}similar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ track_id: trackId }),
})
    .then((response) => response.json())
    .then((data) => {
        similarTrack.value = data.tracks;
    })
    .catch((error) => {
        console.error("Error fetching track:", error);
    });
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
