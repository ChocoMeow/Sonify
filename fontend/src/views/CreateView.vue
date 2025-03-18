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
                    <div class="text-area">
                        <textarea
                            cols="20"
                            rows="5"
                            placeholder="Share the theme genre, mood and key phrases to inspire unique lyrics..."
                            v-model="textarea"
                            :maxlength="maxLength"
                            @input="updateCharacterCount"
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
                    <div class="footer">
                        <Button icon="ifl" name="Random" />
                        <Button
                            icon="draw"
                            name="Generate"
                            backgroundColor="var(--accent)"
                            hoverColor="var(--secondary)"
                            activeColor="var(--secondary-600)"
                        />
                    </div>
                </div>
            </Tab>
            <Tab name="Custom">
                <div class="section">
                    <div class="text-area">
                        <input
                            type="text"
                            maxlength="40"
                            placeholder="Enter a title for your song..."
                        />
                    </div>
                    <div class="header">
                        <h2>Lyrics</h2>
                        <div class="right">
                            <p>Instrumental</p>
                            <Switch v-model="instrumental" />
                        </div>
                    </div>
                    <div class="text-area">
                        <textarea
                            cols="20"
                            rows="15"
                            placeholder="Enter your own lyrics..."
                            v-model="lyricsText"
                            :maxlength="maxLyricsLength"
                            @input="updateLyricsCharacterCount"
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

                    <div class="header">
                        <h2>Style of Music</h2>
                    </div>
                    <div class="text-area">
                        <textarea
                            cols="20"
                            rows="5"
                            placeholder="Enter style of music..."
                            v-model="styleText"
                            :maxlength="maxStyleLength"
                            @input="updateStyleCharacterCount"
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
                            />
                        </div>
                    </div>

                    <div class="footer">
                        <Button icon="cloud_upload" name="Upload Audio" />
                        <Button
                            icon="draw"
                            name="Generate"
                            backgroundColor="var(--accent)"
                            hoverColor="var(--secondary)"
                            activeColor="var(--secondary-600)"
                        />
                    </div>
                </div>
            </Tab>
        </Tabs>
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
import { apiFetch } from "@/auth.js";

// Prompt Tab
const maxLength = ref(200);
const characterCount = ref(0);
const textarea = ref("");

const instrumental = ref(false);
const modelSelected = ref("v2");

// text area word count
const updateCharacterCount = () => {
    characterCount.value = textarea.value.length;
};
watch(textarea, updateCharacterCount);

const onModelSelected = (selected) => {
    modelSelected.value = selected;
};

// Custom Tab
const maxLyricsLength = ref(3000);
const lyricsCharCount = ref(0);
const lyricsText = ref("");

const updateLyricsCharacterCount = () => {
    lyricsCharCount.value = lyricsText.value.length;
};
watch(lyricsText, updateLyricsCharacterCount);

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
const updateStyleCharacterCount = () => {
    styleCharCount.value = styleText.value.length;
};
watch(styleText, updateStyleCharacterCount);

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
                        model: modelSelected.value,
                        prompt,
                    }),
                }
            );
            chatgptLyricsResult.value = data.lyrics;
        } catch (error) {
            console.error("Error fetching lyrics:", error);
        }
        loadingLyrics.value = false;
    }
}
</script>

<style lang="scss" scoped>
.create-view {
    padding: 20px 0;
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
</style>
