<template>
    <div class="dropdown" ref="dropdown">
        <div
            @click="toggleDropdown"
            class="dropdown-button"
            ref="dropdownButton"
        >
            {{ selectedOption }}
            <span
                :class="[
                    'material-symbols-rounded',
                    { rotate: isDropdownOpen },
                ]"
            >
                keyboard_arrow_down
            </span>
        </div>
        <div
            v-if="isDropdownOpen"
            class="dropdown-menu"
            ref="dropdownMenu"
            :style="positionStyle"
        >
            <div
                v-for="option in options"
                :key="option.text"
                class="dropdown-item"
                @click="selectOption(option)"
            >
                <div class="title clamp-text">
                    {{ option.text }}
                    <span
                        class="material-symbols-rounded"
                        v-if="option.text === selectedOption"
                        >check</span
                    >
                </div>
                <div class="option-description clamp-text line2">
                    {{ option.description }}
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick, watch } from "vue";

// Define props
const props = defineProps({
    options: {
        type: Array,
        required: true,
    },
    defaultSelected: {
        type: String,
        required: true,
    },
});

// Define emits
const emit = defineEmits(["optionSelected"]);

const selectedOption = ref(props.defaultSelected);
const isDropdownOpen = ref(false);
const dropdown = ref(null);
const dropdownButton = ref(null);
const dropdownMenu = ref(null);
const positionStyle = ref({});

// Toggle dropdown visibility and update position
const toggleDropdown = () => {
    isDropdownOpen.value = !isDropdownOpen.value;
};

// Select an option
const selectOption = (option) => {
    selectedOption.value = option.text;
    isDropdownOpen.value = false;
    emit("optionSelected", option.text);
};

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
    if (dropdown.value && !dropdown.value.contains(event.target)) {
        isDropdownOpen.value = false;
    }
};

// Update the dropdown menu position based on available viewport space
const updateMenuPosition = () => {
    nextTick(() => {
        if (dropdownMenu.value && dropdownButton.value) {
            // Get the button's bottom position relative to viewport
            const buttonRect = dropdownButton.value.getBoundingClientRect();
            // Get the menu's height
            const menuHeight = dropdownMenu.value.offsetHeight;
            // Available space below and above the button
            const spaceBelow = window.innerHeight - buttonRect.bottom;
            const spaceAbove = buttonRect.top;

            if (spaceBelow < menuHeight && spaceAbove >= menuHeight) {
                // If not enough space below but enough above, position the menu above the button.
                positionStyle.value = {
                    bottom: `${dropdownButton.value.offsetHeight + 8}px`,
                    top: "auto",
                };
            } else {
                // Otherwise, position it below the button.
                positionStyle.value = {
                    top: `${dropdownButton.value.offsetHeight + 8}px`,
                    bottom: "auto",
                };
            }
        }
    });
};

// Watch the dropdown open state to update position when the menu is rendered
watch(isDropdownOpen, (newVal) => {
    if (newVal) {
        updateMenuPosition();
    }
});

// Add/Remove event listeners
onMounted(() => {
    document.addEventListener("click", handleClickOutside);
});

onBeforeUnmount(() => {
    document.removeEventListener("click", handleClickOutside);
});
</script>

<style lang="scss" scoped>
.dropdown {
    position: relative;
    display: inline-block;
    color: var(--text);
    user-select: none;
}

.dropdown-button {
    display: flex;
    align-items: center;
    padding: 8px 20px;
    border: solid 1.5px var(--text);
    border-radius: 50px;
    gap: 4px;
    transition: background-color 0.1s;
    cursor: pointer;

    &:hover {
        background-color: var(--primary-200);
    }
}

.dropdown-menu {
    position: absolute;
    width: 300px;
    max-height: 180px;
    padding: 4px;
    background-color: var(--background-2);
    border-radius: 10px;
    overflow-y: auto;
    z-index: 1;
    box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 2px 6px 2px;
}

.dropdown-item {
    padding: 8px 12px;
    border-radius: 10px;
    cursor: pointer;

    &:hover {
        background-color: var(--primary-200);
    }

    .option-description {
        color: var(--sub-text);
        font-size: 12px;
        font-weight: 300;
    }
}

.title {
    display: flex;
    justify-content: space-between;
    align-items: center;

    span {
        font-size: 20px;
    }
}

.rotate {
    transform: rotate(180deg);
}

.material-symbols-rounded {
    transition: transform 0.1s;
}
</style>
