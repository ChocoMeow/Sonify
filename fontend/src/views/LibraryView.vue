<template>
    <div class="library-view">
        <Tabs>
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
                                    @track-deleted="handleTrackDeleted"
                                />
                            </template>
                            <template v-else-if="trackMessage && !loading">
                                <div class="empty-state">
                                    <img src="@/assets/empty-tracks.svg" alt="No songs" />
                                    <h3>No songs yet</h3>
                                    <p>{{ trackMessage }}</p>
                                    <Button 
                                        icon="music_note_add" 
                                        name="Create a Song" 
                                        backgroundColor="var(--accent)"
                                        hoverColor="var(--secondary)"
                                        activeColor="var(--secondary-600)"
                                        @click="goToCreate" 
                                    />
                                </div>
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
                            <IconButton 
                                v-if="playlists && playlists.length > 0"
                                icon="playlist_add" 
                                backgroundColor="var(--accent)"
                                hoverColor="var(--secondary)"
                                activeColor="var(--secondary-600)"
                                textColor="white"
                                @click="openPlaylistModal"
                            />
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
                        <template v-else-if="playlistMessage && !loading">
                            <div class="empty-state">
                                <img src="@/assets/empty-tracks.svg" alt="No playlists" />
                                <h3>No playlists yet</h3>
                                <p>{{ playlistMessage }}</p>
                                <Button 
                                    icon="playlist_add" 
                                    name="Create a Playlist" 
                                    backgroundColor="var(--accent)"
                                    hoverColor="var(--secondary)"
                                    activeColor="var(--secondary-600)"
                                    @click="openPlaylistModal" 
                                />
                            </div>
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

    <!-- Create Playlist Modal -->
    <DialogModal v-model="showPlaylistModal">
        <div class="create-playlist-modal">
            <h2>Create New Playlist</h2>
            
            <div class="form-group">
                <label for="playlist-name">Playlist Name</label>
                <input 
                    type="text" 
                    id="playlist-name" 
                    v-model="playlistName" 
                    placeholder="Enter playlist name"
                    maxlength="50"
                    :class="{'has-error': errors.name}"
                    @focus="clearError('name')"
                >
                <p v-if="errors.name" class="error-message">{{ errors.name }}</p>
            </div>
            
            <div class="form-group privacy-toggle">
                <label>Privacy Setting</label>
                <div class="toggle-container">
                    <p>Public</p>
                    <Switch v-model="isPrivate" />
                    <p>Private</p>
                </div>
                <p class="helper-text">{{ isPrivate ? 'Only you can see this playlist' : 'Anyone can see this playlist' }}</p>
            </div>
            
            <div class="modal-actions">
                <Button 
                    name="Cancel" 
                    @click="closePlaylistModal"
                />
                <Button 
                    icon="playlist_add" 
                    name="Create Playlist" 
                    backgroundColor="var(--accent)"
                    hoverColor="var(--secondary)"
                    activeColor="var(--secondary-600)"
                    :isLoading="isSubmitting"
                    @click="createPlaylist" 
                />
            </div>
            <p v-if="errors.general" class="error-message general-error">{{ errors.general }}</p>
        </div>
    </DialogModal>
</template>

<script setup>
import Tabs from "@/components/tab/Tabs.vue";
import Tab from "@/components/tab/Tab.vue";
import TrackRow from "@/components/TrackRow.vue";
import TrackRowSkeleton from "@/components/skeleton/TrackRowSkeleton.vue";
import PlaylistCard from "@/components/PlaylistCard.vue";
import PlaylistCardSkeleton from "@/components/skeleton/PlaylistCardSkeleton.vue";
import Button from "@/components/Button.vue";
import IconButton from "@/components/IconButton.vue";
import DialogModal from "@/components/DialogModal.vue";
import Switch from "@/components/Switch.vue";

import { apiFetch } from "@/auth.js";
import { useRouter } from "vue-router";

import { ref, onMounted, watch } from "vue";

const router = useRouter();
const tracks = ref(null);
const playlists = ref(null);
const loading = ref(true);

const trackMessage = ref("");
const playlistMessage = ref("");

// Playlist modal state
const showPlaylistModal = ref(false);
const playlistName = ref("");
const isPrivate = ref(false);
const isSubmitting = ref(false);
const errors = ref({});

// Clear specific error on input focus
const clearError = (field) => {
    if (errors.value[field]) {
        errors.value[field] = '';
    }
};

// Watch to clear name error when editing
watch(playlistName, () => {
    clearError('name');
});

onMounted(async () => {
    loading.value = true;
    await fetchLibraryData();
});

async function fetchLibraryData() {
    try {
        const data = await apiFetch(`${import.meta.env.VITE_API_URL}library`, {
            method: "GET",
        });
        tracks.value = data.tracks || [];
        playlists.value = data.playlists || [];
        
        if (!tracks.value.length) {
            trackMessage.value = "Create your first song and it will appear here.";
        }

        if (!playlists.value.length) {
            playlistMessage.value = "Create a playlist to organize your favorite songs.";
        }
    } catch (error) {
        trackMessage.value = "Error loading library data";
        playlistMessage.value = "Error loading library data";
        console.error(error);
    } finally {
        loading.value = false;
    }
}

function goToCreate() {
    router.push({ name: 'create' });
}

function openPlaylistModal() {
    // Reset form state
    playlistName.value = "";
    isPrivate.value = false;
    errors.value = {};
    showPlaylistModal.value = true;
}

function closePlaylistModal() {
    showPlaylistModal.value = false;
}

async function createPlaylist() {
    // Validate form
    errors.value = {};
    
    if (!playlistName.value.trim()) {
        errors.value.name = "Playlist name is required";
        return;
    }
    
    isSubmitting.value = true;
    
    try {
        // Send API request
        const response = await apiFetch(
            `${import.meta.env.VITE_API_URL}createPlaylist`,
            {
                method: "POST",
                body: JSON.stringify({
                    name: playlistName.value.trim(),
                    isPrivate: isPrivate.value
                }),
            }
        );
        
        // Close modal and refresh playlist data
        closePlaylistModal();
        await fetchLibraryData();
        
    } catch (error) {
        console.error("Error creating playlist:", error);
        
        // Handle API errors
        if (error && error.errors) {
            errors.value = error.errors;
        } else {
            errors.value.general = "Failed to create playlist. Please try again.";
        }
    } finally {
        isSubmitting.value = false;
    }
}

// Add this function to handle track deletion
function handleTrackDeleted(trackId) {
    // Remove the deleted track from the tracks array
    tracks.value = tracks.value.filter(track => track.id !== trackId);
    
    // Show empty state if no tracks left
    if (tracks.value.length === 0) {
        trackMessage.value = "Create your first song and it will appear here.";
    }
}
</script>

<style lang="scss" scoped>
.library-view {
    padding: 20px 0;
}

.sections {
    display: flex;
    flex-direction: column;
    gap: 20px;

    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 10px;
    }

    .playlists {
        display: grid;
        row-gap: 40px;
        grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
    }
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 60px 20px;
    margin: 20px auto;
    max-width: 400px;
    
    img {
        width: 200px;
        height: 200px;
        margin-bottom: 20px;
        opacity: 0.7;
    }
    
    h3 {
        font-size: 1.5rem;
        margin-bottom: 10px;
        color: var(--text);
    }
    
    p {
        margin-bottom: 25px;
        color: var(--sub-text);
        line-height: 1.5;
    }
}

.create-playlist-modal {
    padding: 20px;
    
    h2 {
        text-align: center;
        margin-bottom: 24px;
        color: var(--text);
    }
    
    .form-group {
        margin-bottom: 24px;
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: var(--text);
        }
        
        input {
            width: 100%;
            padding: 12px 16px;
            border-radius: 8px;
            background-color: var(--primary-100);
            border: 1px solid transparent;
            color: var(--text);
            font-size: 16px;
            transition: all 0.2s;
            
            &:focus {
                outline: none;
                border-color: var(--primary);
                box-shadow: 0 0 0 2px rgba(var(--primary-rgb), 0.2);
            }
            
            &.has-error {
                border-color: var(--error);
                box-shadow: 0 0 0 2px rgba(var(--error-rgb), 0.2);
            }
        }
        
        .helper-text {
            margin-top: 8px;
            font-size: 14px;
            color: var(--sub-text);
        }
    }
    
    .privacy-toggle {
        .toggle-container {
            display: flex;
            align-items: center;
            gap: 12px;
            
            p {
                color: var(--sub-text);
            }
        }
    }
    
    .modal-actions {
        display: flex;
        justify-content: flex-end;
        gap: 12px;
        margin-top: 32px;
    }
    
    .error-message {
        color: var(--error);
        font-size: 14px;
        margin-top: 6px;
    }
    
    .general-error {
        text-align: center;
        margin-top: 16px;
    }
}
</style>
