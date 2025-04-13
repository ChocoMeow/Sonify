<template>
    <div class="create-view">
        <Tabs>
            <Tab name="Prompt">
                <div class="section">
                    <div class="header">
                        <h2>Describe your song</h2>
                        <div class="right">
                            <p>Instrumental</p>
                            <Switch v-model="instrumental" />
                        </div>
                    </div>
                    <div class="text-area" :class="{'has-error': errors.prompt_input}">
                        <textarea
                            cols="20"
                            rows="5"
                            placeholder="Share the theme genre, mood and key phrases to inspire unique lyrics..."
                            v-model="textarea"
                            :maxlength="maxLength"
                            @input="updateCharacterCount"
                            @focus="clearError('prompt_input')"
                        ></textarea>
                        <div class="text-area__footer">
                            <Dropdown
                                :options="[
                                    {
                                        text: 'v2',
                                        description:
                                            'With best vocal quality and song structures.',
                                    },
                                    {
                                        text: 'v1',
                                        description:
                                            'Upgraded with better arrangements and creativity.',
                                    },
                                ]"
                                default-selected="v2"
                                @optionSelected="modelSelected"
                            />
                            <p
                                :class="[
                                    characterCount >= maxLength
                                        ? 'reached-max'
                                        : '',
                                ]"
                            >
                                {{ characterCount }} / {{ maxLength }}
                            </p>
                        </div>
                    </div>
                    <p v-if="errors.prompt_input" class="error-message">{{ errors.prompt_input }}</p>
                    
                    <div class="footer">
                        <Button icon="ifl" name="Random" />
                        <Button
                            icon="draw"
                            name="Generate"
                            backgroundColor="var(--accent)"
                            hoverColor="var(--secondary)"
                            activeColor="var(--secondary-600)"
                            @click="submitNormalForm"
                            :isLoading="isSubmitting"
                        />
                    </div>
                </div>
            </Tab>
            <Tab name="Custom">
                <div class="section">
                    <div class="text-area" :class="{'has-error': errors.title}">
                        <input
                            type="text"
                            maxlength="40"
                            placeholder="Enter a title for your song..."
                            v-model="songTitle"
                            @focus="clearError('title')"
                        />
                    </div>
                    <p v-if="errors.title" class="error-message">{{ errors.title }}</p>
                    
                    <div class="header">
                        <h2>Lyrics</h2>
                        <div class="right">
                            <p>Instrumental</p>
                            <Switch v-model="instrumental" />
                        </div>
                    </div>
                    <div class="text-area" :class="{'has-error': errors.lyrics_input}">
                        <textarea
                            cols="20"
                            rows="15"
                            placeholder="Enter your own lyrics..."
                            v-model="lyricsText"
                            :maxlength="maxLyricsLength"
                            @input="updateLyricsCharacterCount"
                            @focus="clearError('lyrics_input')"
                        ></textarea>
                        <div class="text-area__footer">
                            <RoundedButton
                                icon="edit"
                                name="Write Lyrics With ChatGPT"
                                @click="openModal"
                            />
                            <p
                                :class="[
                                    lyricsCharCount >= maxLyricsLength
                                        ? 'reached-max'
                                        : '',
                                ]"
                            >
                                {{ lyricsCharCount }} / {{ maxLyricsLength }}
                            </p>
                        </div>
                    </div>
                    <p v-if="errors.lyrics_input" class="error-message">{{ errors.lyrics_input }}</p>

                    <div class="header">
                        <h2>Style of Music</h2>
                    </div>
                    <div class="text-area" :class="{'has-error': errors.genres_input}">
                        <textarea
                            cols="20"
                            rows="5"
                            placeholder="Enter style of music..."
                            v-model="styleText"
                            :maxlength="maxStyleLength"
                            @input="updateStyleCharacterCount"
                            @focus="clearError('genres_input')"
                        ></textarea>
                        <div
                            class="text-area__footer"
                            style="align-self: flex-end"
                        >
                            <p
                                :class="[
                                    styleCharCount >= 200 ? 'reached-max' : '',
                                ]"
                            >
                                {{ styleCharCount }} / {{ maxStyleLength }}
                            </p>
                        </div>
                        <div class="text-area__scroll">
                            <RoundedButton
                                v-for="style in styles"
                                :key="style"
                                :name="style"
                                @click="addStyle(style)"
                            />
                        </div>
                    </div>
                    <p v-if="errors.genres_input" class="error-message">{{ errors.genres_input }}</p>

                    <div class="footer">
                        <Button icon="cloud_upload" name="Upload Audio" />
                        <Button
                            icon="draw"
                            name="Generate"
                            backgroundColor="var(--accent)"
                            hoverColor="var(--secondary)"
                            activeColor="var(--secondary-600)"
                            @click="submitCustomForm"
                            :isLoading="isSubmitting"
                        />
                    </div>
                </div>
            </Tab>
        </Tabs>
        <div v-if="errors.general" class="error-message general-error">{{ errors.general }}</div>
        <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
    </div>
    <DialogModal v-model="showModal">
        <div class="modal">
            <div class="result-area">
                <div
                    class="select-lyrics"
                    v-if="chatgptLyricsResult && !loadingLyrics"
                    @click="applyLyrics"
                >
                    <p class="lyrics-text">
                        {{ chatgptLyricsResult }}
                    </p>
                </div>

                <div class="no-result" v-else-if="!loadingLyrics">
                    <p>Enter a prompt below to generate lyrics.</p>
                </div>
                <TextBoxSkeleton v-if="loadingLyrics" />
            </div>
            <div class="text-area" @click="focusChatgptLyricsPrompt">
                <textarea
                    cols="20"
                    rows="5"
                    placeholder="Share the theme or topic of the lyrics you're envisioning."
                    ref="chatgptLyricsPrompt"
                    @keydown="handleKeydown"
                />
                <div class="text-area__footer">
                    <Dropdown
                        :options="[
                            {
                                text: 'v2',
                                description:
                                    'With best vocal quality and song structures.',
                            },
                            {
                                text: 'v1',
                                description:
                                    'Upgraded with better arrangements and creativity.',
                            },
                        ]"
                        default-selected="v2"
                        @optionSelected="onModelSelected"
                    />
                    <IconButton
                        icon="arrow_upward"
                        backgroundColor="var(--accent)"
                        @click="submitPrompt"
                        :isLoading="loadingLyrics"
                    />
                </div>
            </div>
        </div>
    </DialogModal>
</template>

<script setup>
import Tabs from "@/components/tab/Tabs.vue";
import Tab from "@/components/tab/Tab.vue";
import Switch from "@/components/Switch.vue";
import Dropdown from "@/components/Dropdown.vue";
import Button from "@/components/Button.vue";
import RoundedButton from "@/components/RoundedButton.vue";
import IconButton from "@/components/IconButton.vue";
import DialogModal from "@/components/DialogModal.vue";
import TextBoxSkeleton from "@/components/skeleton/TextBoxSkeleton.vue";

import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import { apiFetch } from "@/auth.js";

// Initialize router
const router = useRouter();

// Prompt Tab
const maxLength = ref(200);
const characterCount = ref(0);
const textarea = ref("");

const instrumental = ref(false);
const selectedModel = ref("v2");

// Custom Tab
const songTitle = ref("");
const maxLyricsLength = ref(3000);
const lyricsCharCount = ref(0);
const lyricsText = ref("");

const maxStyleLength = ref(200);
const styleCharCount = ref(0);
const styleText = ref("");
const styles = ref([
    "romantic",
    "upbeat",
    "melancholic",
    "hopeful",
    "mysterious",
    "nostalgic",
    "playful",
]);

// Form handling
const errors = ref({});
const isSubmitting = ref(false);
const successMessage = ref("");

// Clear specific error on input focus
const clearError = (field) => {
    if (errors.value[field]) {
        errors.value[field] = '';
    }
};

// text area word count
const updateCharacterCount = () => {
    characterCount.value = textarea.value.length;
    clearError('prompt_input');
};
watch(textarea, updateCharacterCount);

const modelSelected = (selected) => {
    selectedModel.value = selected;
};

const updateLyricsCharacterCount = () => {
    lyricsCharCount.value = lyricsText.value.length;
    clearError('lyrics_input');
};
watch(lyricsText, updateLyricsCharacterCount);

const updateStyleCharacterCount = () => {
    styleCharCount.value = styleText.value.length;
    clearError('genres_input');
};
watch(styleText, updateStyleCharacterCount);

// Watch to clear title error when editing
watch(songTitle, () => {
    clearError('title');
});

// Add style when clicking style button
const addStyle = (style) => {
    if (styleText.value.length === 0) {
        styleText.value = style;
    } else if (!styleText.value.includes(style)) {
        styleText.value += `, ${style}`;
    }
    clearError('genres_input');
};

// Form submission
async function submitNormalForm() {
    // Clear previous errors and success message
    errors.value = {};
    successMessage.value = "";
    
    // Create payload
    const payload = {
        mode: "normal",
        model: selectedModel.value,
        isInstrumental: instrumental.value,
        prompt_input: textarea.value
    };
    
    // Submit form
    await submitForm(payload);
}

async function submitCustomForm() {
    // Clear previous errors and success message
    errors.value = {};
    successMessage.value = "";
    
    // Create payload
    const payload = {
        mode: "custom",
        model: selectedModel.value,
        isInstrumental: instrumental.value,
        title: songTitle.value,
        lyrics_input: lyricsText.value,
        genres_input: styleText.value
    };
    
    // Submit form
    await submitForm(payload);
}

async function submitForm(payload) {
    try {
        isSubmitting.value = true;
        errors.value = {}; // Clear previous errors
        
        const response = await fetch(
            `${import.meta.env.VITE_API_URL}createTrack`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    ...(localStorage.getItem("token") && { 
                        Authorization: `Bearer ${localStorage.getItem("token")}` 
                    }),
                },
                body: JSON.stringify(payload),
            }
        );
        
        const data = await response.json();
        
        if (!response.ok) {
            // Handle error response
            if (data.errors) {
                errors.value = data.errors;
            } else {
                errors.value = { general: data.message || "An error occurred" };
            }
            isSubmitting.value = false; // Only set to false on error
            return;
        }
        
        // Handle successful submission
        successMessage.value = "Song generation started successfully!";
        
        setTimeout(() => {
            // Redirect to library page
            router.push({ name: "library" });
            // We don't set isSubmitting to false here since we're redirecting
        }, 1500);
        
    } catch (error) {
        console.error("Error submitting form:", error);
        errors.value = { general: "Failed to connect to the server. Please try again." };
        isSubmitting.value = false; // Only set to false on error
    }
}

// Modal
const loadingLyrics = ref(false);
const chatgptLyricsResult = ref();
const chatgptLyricsPrompt = ref();
const showModal = ref(false);

function focusChatgptLyricsPrompt() {
    chatgptLyricsPrompt.value.focus();
}

function openModal() {
    showModal.value = true;
    setTimeout(() => {
        focusChatgptLyricsPrompt();
    }, 200);
}

function applyLyrics() {
    lyricsText.value = chatgptLyricsResult.value;
    showModal.value = false;
}

async function handleKeydown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        await submitPrompt();
    }
}

async function submitPrompt() {
    const prompt = chatgptLyricsPrompt.value.value.trim();
    if (prompt) {
        try {
            loadingLyrics.value = true;
            const data = await apiFetch(
                `${import.meta.env.VITE_API_URL}generateLyrics`,
                {
                    method: "POST",
                    body: JSON.stringify({
                        model: selectedModel.value,
                        prompt,
                    }),
                }
            );
            chatgptLyricsResult.value = data.lyrics;
        } catch (error) {
            console.error("Error fetching lyrics:", error);
        } finally {
            loadingLyrics.value = false;
        }
    }
}

// For dropdown in the chatgpt modal
const onModelSelected = (selected) => {
    selectedModel.value = selected;
};
</script>

<style lang="scss" scoped>
.create-view {
    padding: 20px 0;
    position: relative;
}

.section {
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.header {
    display: flex;
    margin-top: 10px;
    justify-content: space-between;
    align-items: center;
    z-index: 0;

    p {
        color: var(--sub-text);
    }

    .right {
        display: flex;
        align-items: center;
        gap: 10px;
    }
}

.text-area {
    display: flex;
    flex-direction: column;
    padding: 20px;
    background-color: var(--primary-100);
    border-radius: 10px;
    transition: all 0.1s;
    box-shadow: var(--primary-200) 0px 0px 5px 0px,
        var(--primary-200) 0px 0px 1px 0px;

    &:hover {
        box-shadow: var(--primary-500) 0px 0px 5px 0px,
            var(--primary-500) 0px 0px 1px 0px;
    }

    &:focus-within,
    &:active {
        box-shadow: var(--primary) 0px 0px 5px 0px,
            var(--primary) 0px 0px 1px 0px;
    }
    
    &.has-error {
        box-shadow: var(--error) 0px 0px 5px 0px,
            var(--error) 0px 0px 1px 0px;
            
        &:hover, &:focus-within, &:active {
            box-shadow: var(--error) 0px 0px 5px 0px,
                var(--error) 0px 0px 1px 0px;
        }
    }

    input,
    textarea {
        outline: none;
        border: none;
        resize: none;
        background: none;
        color: var(--text);
        font-size: 16px;
    }

    &__scroll {
        display: flex;
        gap: 10px;
        overflow: auto;
        padding-top: 10px;
    }

    &__footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-top: 20px;
        color: var(--sub-text);

        .reached-max {
            color: var(--error);
        }
    }
}

.footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 50px;
}

.modal {
    .result-area {
        display: flex;
        width: 100%;
        height: 55svh;
        color: var(--sub-text);
        overflow: hidden;

        .select-lyrics {
            width: 100%;
            height: 100%;
            padding: 10px;
            border-radius: 10px;
            overflow-y: auto;
            transition: background-color .1s;
            cursor: pointer;

            &:hover {
                background-color: var(--primary-100);
            }
        }

        .lyrics-text {
            white-space: pre-wrap;
            color: var(--text);
            border-radius: 10px;
        }

        .no-result {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }
    }

    .text-area {
        margin-top: 20px;
        cursor: text;
        textarea {
            field-sizing: content;
            max-height: 80px;
        }
    }

    ::-webkit-scrollbar-thumb {
        background-color: var(--primary-100);
    }
}

.error-message {
    color: var(--error);
    font-size: 14px;
    margin-top: -15px;
    margin-bottom: 15px;
}

.success-message {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background-color: var(--accent);
    color: white;
    padding: 12px 20px;
    border-radius: 10px;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
    z-index: 100;
    animation: fadeIn 0.3s, fadeOut 0.3s 5s forwards;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translate(-50%, 20px); }
    to { opacity: 1; transform: translate(-50%, 0); }
}

@keyframes fadeOut {
    from { opacity: 1; transform: translate(-50%, 0); }
    to { opacity: 0; transform: translate(-50%, 20px); }
}

.general-error {
    padding: 12px 20px;
    margin: 15px auto;
    max-width: 90%;
    text-align: center;
    background-color: rgba(var(--error-rgb), 0.1);
    border-radius: 10px;
}
</style>
