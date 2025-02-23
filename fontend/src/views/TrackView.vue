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
                            <TrackRow
                                :isLarge="false"
                                v-for="track in similarTrack"
                                :key="track"
                                :track="track"
                            />
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

import { ref } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const trackId = route.params.id;

defineProps({
    track: {
        type: Object,
        default: () => ({
            id: "",
            title: "Midnight Mirage",
            duration: "3:12",
            prompt: "Jazz, Techno, Goa Trance, Blues",
            thumbnail:
                "https://cdn2.suno.ai/f53aae83-57b8-463d-afd0-7cef8f67e43c_bfd29f65.jpeg",
            lyrics: "(Verse 1) \nSlow burn, deep sigh, (ahh, yeah) \nHeat rising under neon lights. \nSilk touch, whispered lies, (mm, so close) \nYou pull me in, then say goodbye. \n\n(Pre-Chorus) \nOoh, the bassline’s got me hypnotized, (oh, oh, oh) \nYour shadow lingers in my mind. \nOne taste of you, I lose my way, (mmm, can't fight it) \nFalling deeper night by night. \n\n(Chorus) \nMove slow, feel the fire, (oh yeah, just like that) \nLet the rhythm take you higher. \nDrunk on you, no escape, (uh-huh, no escape) \nA midnight mirage, I fade away. (ahh, yeah) \n\n(Verse 2) \nGold chains, midnight haze, (mm, midnight) \nYour perfume lingers in the maze. \nVelvet secrets, lips so bold, (ah-ha, dangerous) \nA touch too hot, a heart too cold. \n\n(Bridge) \nOh, don’t say my name, just let it flow, (shh, just feel it) \nWe dance like we got nowhere to go. \nFading echoes, burning bright, (mmm, yeah) \nLost in love, lost in night. \n\n(Chorus) \nMove slow, feel the fire, (ahh, don't stop) \nLet the rhythm take you higher. \nDrunk on you, no escape, (mmm, so high) \nA midnight mirage, I fade away. (yeah, fade away) \n\n(Outro) \nSlow burn, deep sigh, (ah-ha, ohh) \nHeat rising under neon lights... END",
            author: {
                avatarUrl: "https://cdn1.suno.ai/4d737235.webp",
                name: "Stealth Noise Spider",
            },
        }),
    },
});

const track = ref(null);
const similarTrack = ref(null);

fetch(`http://127.0.0.1:5000/api/track`, {
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

fetch(`http://127.0.0.1:5000/api/similar`, {
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
