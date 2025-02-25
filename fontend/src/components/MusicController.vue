<template>
    <div :class="['audio-player', { show: currentTrack }]">
        <audio
            ref="audioRef"
            :src="currentTrack?.src"
            @ended="onTrackEnded"
            @loadedmetadata="onLoadedMetadata"
        ></audio>
        <div class="track">
            <img :src="currentTrack?.thumbnail" alt="" />
            <div class="info">
                <router-link
                    :to="{ name: 'create', params: { id: currentTrack?.id } }"
                >
                    <p class="clamp-text">
                        {{ currentTrack?.title || "No Track Selected" }}
                    </p>
                </router-link>
                <div class="author-info">
                    <img :src="currentTrack?.author.avatarUrl" alt="" />
                    <p class="clamp-text">{{ currentTrack?.author.name }}</p>
                </div>
            </div>
        </div>
        <div class="center">
            <div class="controls">
                <IconButton icon="skip_previous" @click="prevTrack" />
                <IconButton icon="fast_rewind" @click="rewind" />
                <IconButton
                    icon="play_arrow"
                    v-if="!state.isPlaying"
                    @click="play"
                />
                <IconButton icon="pause" v-else @click="pause" />
                <IconButton icon="fast_forward" @click="fastForward" />
                <IconButton icon="skip_next" @click="nextTrack" />
            </div>
            <div class="progress-container">
                <span>{{ formatTime(currentTime) }}</span>
                <input
                    type="range"
                    min="0"
                    :max="duration"
                    :value="currentTime"
                    @input="setCurrentTime"
                />
                <span>{{ formatTime(duration) }}</span>
            </div>
        </div>
        <div class="actions">
            <IconButton icon="favorite" />

            <div ref="volumeButtonRef" class="volume-container">
                <div
                    v-if="showVolumePopup"
                    ref="volumePopupRef"
                    class="volume-popup"
                >
                    <input
                        type="range"
                        min="0"
                        max="1"
                        step="0.01"
                        v-model.number="volume"
                        @input="updateVolume"
                        class="vertical-range"
                    />
                </div>
                <IconButton icon="volume_up" @click="toggleVolumePopup" />
            </div>

            <IconButton icon="more_vert" />
        </div>
    </div>
</template>

<script setup>
import IconButton from "@/components/IconButton.vue";
import { ref, watch, onMounted, onBeforeUnmount } from "vue";
import { useAudioPlayer } from "@/composables/useAudioPlayer";

const { state, currentTrack, audioRef } = useAudioPlayer();
const currentTime = ref(0);
const duration = ref(0);
const volume = ref(1);
const showVolumePopup = ref(false);

const volumePopupRef = ref(null);
const volumeButtonRef = ref(null);

const play = () => {
    if (audioRef.value) {
        audioRef.value.play();
        state.isPlaying = true;
    }
};

const pause = () => {
    if (audioRef.value) {
        audioRef.value.pause();
        state.isPlaying = false;
    }
};

const onLoadedMetadata = () => {
    if (audioRef.value) {
        duration.value = audioRef.value.duration || 0;
        audioRef.value.volume = volume.value;
    }
};

watch(currentTrack, (newTrack) => {
    if (newTrack && audioRef.value) {
        resetAudio();
        if (state.isPlaying) {
            play();
        }
    }
});

const formatTime = (time) => {
    if (isNaN(time) || time < 0) return "0:00";
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
};

const setCurrentTime = (event) => {
    if (audioRef.value) {
        audioRef.value.currentTime = event.target.value;
    }
};

const updateCurrentTime = () => {
    if (audioRef.value) {
        currentTime.value = audioRef.value.currentTime;
    }
};

const updateVolume = () => {
    if (audioRef.value) {
        audioRef.value.volume = volume.value;
    }
};

let timeInterval = null;
onMounted(() => {
    timeInterval = setInterval(updateCurrentTime, 1000);
    document.addEventListener("click", handleClickOutside);
});

onBeforeUnmount(() => {
    clearInterval(timeInterval);
    document.removeEventListener("click", handleClickOutside);
});

const nextTrack = () => {
    if (state.currentIndex < state.queue.length - 1) {
        state.currentIndex++;
        resetAudio();
        play();
    }
};

const prevTrack = () => {
    if (state.currentIndex > 0) {
        state.currentIndex--;
        resetAudio();
        play();
    }
};

const fastForward = () => {
    if (audioRef.value && audioRef.value.duration) {
        audioRef.value.currentTime = Math.min(
            audioRef.value.duration,
            audioRef.value.currentTime + 10
        );
    }
};

const rewind = () => {
    if (audioRef.value) {
        audioRef.value.currentTime = Math.max(
            0,
            audioRef.value.currentTime - 10
        );
    }
};

const resetAudio = () => {
    if (audioRef.value) {
        audioRef.value.load();
    }
};

const onTrackEnded = () => {
    nextTrack();
};

const toggleVolumePopup = () => {
    showVolumePopup.value = !showVolumePopup.value;
};

const handleClickOutside = (event) => {
    const volumePopupEl = volumePopupRef.value;
    const volumeButtonEl = volumeButtonRef.value;
    if (
        showVolumePopup.value &&
        volumePopupEl &&
        !volumePopupEl.contains(event.target) &&
        volumeButtonEl &&
        !volumeButtonEl.contains(event.target)
    ) {
        showVolumePopup.value = false;
    }
};
</script>

<style lang="scss" scoped>
.audio-player {
    position: absolute;
    width: 100%;
    bottom: 0px;
    padding: 1rem;
    display: flex;
    align-items: center;
    z-index: 1;
    border-radius: 10px;
    background-color: var(--background);
    box-shadow: var(--primary) 0px 0px 5px 0px, var(--primary) 0px 0px 1px 0px;
    opacity: 0;
    pointer-events: none;
    transition: all 0.2s;

    &.show {
        opacity: 1;
        pointer-events: all;
        bottom: 10px;
    }
}

.track {
    width: 25%;
    display: flex;
    align-items: center;
    gap: 18px;

    img {
        width: 68px;
        height: 68px;
        border-radius: 10px;
    }

    .info {
        display: flex;
        flex-direction: column;
        gap: 12px;

        p {
            font-weight: 500;
            &:hover {
                text-decoration: underline;
            }
        }

        .author-info {
            display: flex;
            gap: 8px;

            img {
                width: 20px;
                height: 20px;
                border-radius: 50%;
            }

            p {
                font-size: small;
                font-weight: 300;
                color: var(--sub-text);
            }
        }
    }
}

.center {
    width: 50%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.controls {
    display: flex;
    gap: 10px;
    margin: 0 auto;
    justify-content: center;
}

.progress-container {
    display: flex;
    align-items: center;
    width: 100%;
    margin: 10px 0;

    input[type="range"] {
        flex: 1;
        margin: 0 10px;
        -webkit-appearance: none;
        appearance: none;
        width: 100%;
        cursor: pointer;
        outline: none;
        border-radius: 15px;
        height: 6px;
        background: var(--primary-200);

        &::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            height: 15px;
            width: 15px;
            background-color: var(--primary);
            border-radius: 50%;
            border: none;
            transition: 0.2s ease-in-out;
        }

        &::-moz-range-thumb {
            height: 15px;
            width: 15px;
            background-color: var(--primary);
            border-radius: 50%;
            border: none;
            transition: 0.2s ease-in-out;
        }
    }
}

.actions {
    width: 25%;
    display: flex;
    gap: 10px;
    justify-content: flex-end;

    .volume-container {
        position: relative;
        display: inline-block;
    }

    .volume-popup {
        position: absolute;
        bottom: 120%;
        left: 50%;
        transform: translateX(-50%);
        background: var(--background);
        padding: 5px;
        border-radius: 5px;
        z-index: 2;
        display: flex;
        justify-content: center;
        align-items: center;

        input[type="range"] {
            width: 100px;
            -webkit-appearance: none;
            appearance: none;
            cursor: pointer;
            outline: none;
            border-radius: 20px;
            background: var(--primary-200);

            &::-webkit-slider-thumb {
                -webkit-appearance: none;
                appearance: none;
                width: 12px;
                height: 12px;
                background: var(--primary);
                border-radius: 50%;
            }

            &::-moz-range-thumb {
                width: 12px;
                height: 12px;
                background: var(--primary);
                border-radius: 50%;
            }
        }
    }
}
</style>
