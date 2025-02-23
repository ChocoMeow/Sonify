import { reactive, computed, ref } from "vue";

const audioRef = ref(null);

const state = reactive({
    queue: [],
    currentIndex: 0,
    isPlaying: false,
});

function addTrack(track) {
    state.queue.push(track);
}

function playTrackAtIndex(index) {
    if (index >= 0 && index < state.queue.length) {
        state.currentIndex = index;
    }
}

export function useAudioPlayer() {
    const currentTrack = computed(
        () => state.queue[state.currentIndex] || null
    );

    return {
        state,
        audioRef,
        addTrack,
        playTrackAtIndex,
        currentTrack,
    };
}
