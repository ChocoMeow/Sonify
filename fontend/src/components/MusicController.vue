<template>
    <div :class="['audio-player', { show: currentTrack }]">
        <audio
            ref="audioRef"
            :src="currentTrack?.src"
            @ended="onTrackEnded"
            @loadedmetadata="updateDuration"
        ></audio>
        <div class="track">
            <img :src="currentTrack?.thumbnail" alt="" />
            <div class="info">
                <p class="clamp-text">
                    {{ currentTrack?.title || "No Track Selected" }}
                </p>
                <div class="author-info">
                    <img :src="currentTrack?.author.avatarUrl" alt="" />
                    <p class="clamp-text">{{ currentTrack?.author.name }}</p>
                </div>
            </div>
        </div>
        <div class="center">
            <div class="controls">
                <IconButton
                    icon="skip_previous"
                    @click="prevTrack"
                ></IconButton>
                <IconButton icon="fast_rewind" @click="rewind"></IconButton>
                <IconButton
                    icon="play_arrow"
                    v-if="!state.isPlaying"
                    @click="play"
                ></IconButton>
                <IconButton icon="pause" v-else @click="pause"></IconButton>
                <IconButton
                    icon="fast_forward"
                    @click="fastForward"
                ></IconButton>
                <IconButton icon="skip_next" @click="nextTrack"></IconButton>
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
            <IconButton icon="volume_up" />
            <IconButton icon="more_vert" />
        </div>
    </div>
</template>

<script setup>
import IconButton from "@/components/IconButton.vue";
import { watch, ref, computed } from "vue";
import { useAudioPlayer } from "@/composables/useAudioPlayer";

const { state, currentTrack, audioRef } = useAudioPlayer();
const currentTime = ref(0);
const duration = ref(0);

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

// Update current time and duration when track changes
watch(currentTrack, (newTrack) => {
    if (newTrack && audioRef.value) {
        resetAudio();
        duration.value = audioRef.value.duration;
        if (state.isPlaying) {
            play();
        }
    }
});

// Format time for display (MM:SS)
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

const updateDuration = () => {
    if (audioRef.value) {
        duration.value = audioRef.value.duration || 0; // Ensure it's a number
    }
};

// Update current time every second
setInterval(updateCurrentTime, 1000);

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
</script>

<style lang="scss" scoped>
.audio-player {
    position: sticky;
    width: 100%;
    bottom: -20px;
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
    justify-content: end;
}

</style>
