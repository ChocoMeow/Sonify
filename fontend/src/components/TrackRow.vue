<template>
    <div :class="['track', { small: !isLarge }]" @click="toggleTrack(track)">
        <div class="track-info">
            <p class="rank" v-if="rank">{{ rank }}</p>
            <div class="image-container">
                <img :src="track.thumbnail" alt="" />
                <div class="waves" v-if="isThisTrackPlaying">
                    <div class="wave" v-for="n in 3" :key="n"></div>
                </div>
            </div>
            <div class="detail">
                <router-link
                    :to="{ name: 'track', params: { id: track.id } }"
                    @click.stop="handleLinkClick"
                >
                    <h3 class="track-title clamp-text">{{ track.title }}</h3>
                </router-link>
                <p class="clamp-text">{{ track.prompt }}</p>
                <div class="author">
                    <img :src="track.author.avatarUrl" alt="" />
                    <p>{{ track.author.name }}</p>
                </div>
            </div>
        </div>
        <div class="right">
            <div class="likes" v-if="isLarge">
                <span class="material-symbols-rounded"> thumb_up </span>
                <p>{{ track.likes }}</p>
            </div>
            <p>{{ track.duration }}</p>
            <span class="material-symbols-rounded action" v-if="isLarge">
                favorite
            </span>
            <span 
                class="material-symbols-rounded action" 
                v-if="isLarge" 
                @click.stop="openContextMenu"
                ref="menuButton"
            >
                more_horiz
            </span>
        </div>
        
        <!-- Context Menu -->
        <div 
            v-if="showContextMenu" 
            class="context-menu"
            :style="menuPosition"
            ref="contextMenu"
        >
            <div class="menu-item" @click.stop="handlePlayNow(track)">
                <span class="material-symbols-rounded">play_arrow</span>
                <p>Play Now</p>
            </div>
            <div class="menu-item" @click.stop="handleAddToQueue(track)">
                <span class="material-symbols-rounded">queue_music</span>
                <p>Add to Queue</p>
            </div>
            <div class="menu-item" @click.stop="handlePlayNext(track)">
                <span class="material-symbols-rounded">queue_play_next</span>
                <p>Play Next</p>
            </div>
            <div class="menu-divider" v-if="isCurrentUserAuthor"></div>
            <div class="menu-item delete" @click.stop="confirmDeleteTrack" v-if="isCurrentUserAuthor">
                <span class="material-symbols-rounded">delete</span>
                <p>Delete Track</p>
            </div>
        </div>
    </div>
    
    <!-- Delete Confirmation Modal -->
    <DialogModal v-model="showDeleteModal">
        <div class="delete-modal">
            <h3>Delete Track</h3>
            <p>Are you sure you want to delete "{{ track.title }}"? This action cannot be undone.</p>
            <div class="modal-actions">
                <Button name="Cancel" @click="showDeleteModal = false" />
                <Button 
                    name="Delete" 
                    icon="delete"
                    backgroundColor="var(--error)"
                    :isLoading="isDeleting"
                    @click="deleteTrack" 
                />
            </div>
        </div>
    </DialogModal>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted, watch, nextTick } from "vue";
import { useAudioPlayer } from "@/composables/useAudioPlayer";
import { authState, apiFetch } from "@/auth.js";
import Button from "@/components/Button.vue";
import DialogModal from "@/components/DialogModal.vue";

const props = defineProps({
    rank: {
        type: String,
        default: "",
    },
    isLarge: {
        type: Boolean,
        default: true,
    },
    track: {
        type: Object,
        default: () => ({
            id: "",
            title: "",
            prompt: "",
            thumbnail: "",
            duration: "",
            likes: 0,
            author: {
                avatarUrl: "",
                name: "",
                userId: "",
            },
        }),
    },
});

const emits = defineEmits(['trackDeleted']);

const { state, audioRef, playTrack, currentTrack, addTrack } = useAudioPlayer();

// Context menu state
const showContextMenu = ref(false);
const menuPosition = ref({ top: '0px', left: '0px' });
const menuButton = ref(null);
const contextMenu = ref(null);

// Delete modal state
const showDeleteModal = ref(false);
const isDeleting = ref(false);

const isThisTrackPlaying = computed(() => {
    return (
        state.isPlaying &&
        state.queue[state.currentIndex]?.id === props.track?.id
    );
});

const isCurrentUserAuthor = computed(() => {
    return authState.currentUser.userId === props.track.author.id;
});

const handleLinkClick = (event) => {
    event.preventDefault();
};

const toggleTrack = (track) => {
    if (currentTrack.value?.id === track.id) {
        const isPlaying = state.isPlaying;
        isPlaying ? audioRef.value.pause() : audioRef.value.play();
        state.isPlaying = !isPlaying;
    } else {
        playTrack(track);
    }
}

// Close context menu when scrolling
const handleScroll = () => {
    if (showContextMenu.value) {
        closeContextMenu();
    }
};

// Close context menu when another track is selected
watch(() => currentTrack.value?.id, (newTrackId, oldTrackId) => {
    if (showContextMenu.value && newTrackId !== oldTrackId) {
        closeContextMenu();
    }
});

// Context menu functions
const openContextMenu = (event) => {
    event.stopPropagation();
    
    // Close any other open menus first
    closeAllMenus();
    
    // Get menu button position
    const buttonRect = menuButton.value.getBoundingClientRect();
    
    // First set menu to default position to make it visible
    menuPosition.value = {
        top: `${buttonRect.bottom}px`,
        left: `${buttonRect.left - 150}px`  // Offset to align menu to the left of the button
    };
    
    // Make menu visible
    showContextMenu.value = true;
    
    // Use nextTick to calculate proper position after menu is rendered
    nextTick(() => {
        if (!contextMenu.value) return;
        
        const menuRect = contextMenu.value.getBoundingClientRect();
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;
        
        // Default position (below and to the left of the button)
        let top = buttonRect.bottom;
        let left = buttonRect.left - 150; // Offset to align menu
        
        // Check right edge - if menu would go off-screen, align to right edge of window
        if (left + menuRect.width > windowWidth) {
            left = windowWidth - menuRect.width - 10; // 10px padding
        }
        
        // Check left edge - if menu would go off-screen, align to left edge of window
        if (left < 10) {
            left = 10; // 10px padding
        }
        
        // Check bottom edge - if menu would go off-screen, position above the button
        if (top + menuRect.height > windowHeight) {
            top = buttonRect.top - menuRect.height;
            
            // If still off-screen at the top, position at the top of the screen with padding
            if (top < 10) {
                top = 10;
            }
        }
        
        // Update menu position with calculated values
        menuPosition.value = {
            top: `${top}px`,
            left: `${left}px`
        };
    });
    
    // Listen for clicks outside menu to close it
    document.addEventListener('click', closeContextMenu);
    // Add scroll listener
    window.addEventListener('scroll', handleScroll, true);
};

const closeContextMenu = () => {
    showContextMenu.value = false;
    document.removeEventListener('click', closeContextMenu);
    window.removeEventListener('scroll', handleScroll, true);
};

// Close all context menus in the app (for use when opening a new one)
const closeAllMenus = () => {
    // Create a custom event to tell other TrackRow components to close their menus
    const closeMenuEvent = new CustomEvent('closeAllContextMenus');
    document.dispatchEvent(closeMenuEvent);
};

// Menu actions
const handlePlayNow = (track) => {
    playTrack(track);
    closeContextMenu();
};

const handleAddToQueue = (track) => {
    addTrack(track);
    closeContextMenu();
};

const handlePlayNext = (track) => {
    // Add track just after the current playing track
    const newIndex = state.currentIndex + 1;
    state.queue.splice(newIndex, 0, track);
    closeContextMenu();
};

const confirmDeleteTrack = () => {
    closeContextMenu();
    showDeleteModal.value = true;
};

const deleteTrack = async () => {
    isDeleting.value = true;
    try {
        await apiFetch(`${import.meta.env.VITE_API_URL}removeTrack`, {
            method: "POST",
            body: JSON.stringify({
                trackId: props.track.id
            }),
        });
        
        showDeleteModal.value = false;
        
        // Emit event to parent component to refresh track list
        emits('trackDeleted', props.track.id);
        
    } catch (error) {
        console.error("Failed to delete track:", error);
        // You could add error handling UI here
    } finally {
        isDeleting.value = false;
    }
};

// Register and unregister event listeners
onMounted(() => {
    // Listen for the closeAllContextMenus event
    document.addEventListener('closeAllContextMenus', handleCloseAllMenus);
});

onUnmounted(() => {
    document.removeEventListener('click', closeContextMenu);
    window.removeEventListener('scroll', handleScroll, true);
    document.removeEventListener('closeAllContextMenus', handleCloseAllMenus);
});

// Handler for closeAllContextMenus event
const handleCloseAllMenus = () => {
    showContextMenu.value = false;
};
</script>

<style lang="scss" scoped>
.track {
    display: flex;
    justify-content: space-between;
    padding: 12px 20px;
    border-radius: 10px;
    transition: background-color 0.1s;
    gap: 20px;
    cursor: pointer;
    position: relative;

    &:hover {
        background-color: var(--primary-200);
    }

    &.small {
        padding: 4px 8px;
    }

    .track-info {
        display: flex;
        align-items: center;
        gap: 20px;
        width: 100%;

        .image-container {
            position: relative;
            min-width: 68px;
            height: 68px;
            border-radius: 10px;
            overflow: hidden;
        }

        img {
            width: 68px;
            height: 68px;
            border-radius: 10px;
        }

        .rank {
            font-size: 25px;
            font-weight: 700;
            color: var(--sub-text);
            letter-spacing: 2px;
        }

        .detail {
            display: flex;
            flex-direction: column;

            p {
                font-size: 12px;
                color: var(--sub-text);
            }

            .track-title {
                &:hover {
                    text-decoration: underline;
                }
            }
        }

        .author {
            display: flex;
            align-items: center;
            margin: 5px 0;
            gap: 10px;

            img {
                width: 20px;
                height: 20px;
            }
        }
    }

    .right {
        display: flex;
        align-items: center;
        gap: 25px;

        .likes {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .action {
            transition: scale 0.1s;
            &:hover {
                scale: 1.1;
            }
            &:active {
                scale: 0.9;
            }
        }
    }
}

.context-menu {
    position: fixed;
    min-width: 180px;
    background-color: var(--background-2);
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    z-index: 1000;
    overflow: hidden;
    
    .menu-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        cursor: pointer;
        transition: background-color 0.1s;
        
        &:hover {
            background-color: var(--primary-100);
        }
        
        p {
            font-size: 14px;
            color: var(--text);
        }
        
        &.delete {
            color: var(--error);
            
            p {
                color: var(--error);
            }
        }
    }
    
    .menu-divider {
        height: 1px;
        background-color: var(--primary-200);
        margin: 4px 0;
    }
}

.delete-modal {
    padding: 24px;
    
    h3 {
        margin-bottom: 16px;
        color: var(--text);
    }
    
    p {
        color: var(--sub-text);
        margin-bottom: 24px;
        line-height: 1.5;
    }
    
    .modal-actions {
        display: flex;
        justify-content: flex-end;
        gap: 12px;
    }
}

.waves {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5px;
    background-color: var(--background-500);
    --_m: 10;

    .wave {
        aspect-ratio: 0.185/1;
        background-color: var(--text);
        border-radius: 15px;
        width: 5px;

        &:nth-child(1) {
            animation: waveform calc(200ms * var(--_m)) ease-in-out infinite
                forwards;
        }
        &:nth-child(2) {
            animation: waveform calc(100ms * var(--_m)) ease-in-out infinite
                forwards;
        }
        &:nth-child(3) {
            animation: waveform calc(500ms * var(--_m)) ease-in-out infinite
                forwards;
        }
    }
}

@keyframes waveform {
    0% {
        transform: scaleY(0.4);
    }
    50% {
        transform: scaleY(1);
    }
    100% {
        transform: scaleY(0.4);
    }
}
</style>
