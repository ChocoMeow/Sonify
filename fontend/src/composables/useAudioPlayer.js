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
        
        if (audioRef.value) {
            const currentTrack = state.queue[state.currentIndex];
            audioRef.value.src = currentTrack.src;
            audioRef.value.load();
            
            state.isPlaying = true;
            audioRef.value.play()
                .catch(err => console.error("Playback failed:", err));
        }
    }
}

function playTrack(track) {
    const existingIndex = state.queue.findIndex((t) => t.src === track.src);

    if (existingIndex === -1) {
        addTrack(track);
        state.currentIndex = state.queue.length - 1;
    } else {
        state.currentIndex = existingIndex;
    }

    if (audioRef.value) {
        const currentTrack = state.queue[state.currentIndex];
        audioRef.value.src = currentTrack.src;
        audioRef.value.load();

        audioRef.value.addEventListener(
            "canplay",
            () => {
                state.isPlaying = true;
                audioRef.value
                    .play()
                    .catch((err) => console.error("Playback failed:", err));
            },
            { once: true }
        );
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
        playTrack,
        currentTrack,
    };
}
