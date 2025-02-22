<template>
    <div
        class="btn"
        :class="{ toggle: isToggle }"
        :style="{ backgroundColor: computedBackgroundColor }"
        @mouseover="hovering = true"
        @mouseleave="hovering = false"
        @mousedown="active = true"
        @mouseup="active = false"
    >
        <span v-if="icon" class="material-symbols-rounded fill">{{
            icon
        }}</span>
        {{ name }}
    </div>
</template>

<script setup>
import { ref, computed } from "vue";

const props = defineProps({
    icon: {
        type: String,
        default: "",
    },
    name: {
        type: String,
        default: "Button",
    },
    isToggle: {
        type: Boolean,
        default: false,
    },
    backgroundColor: {
        type: String,
        default: "var(--primary-100)",
    },
    hoverColor: {
        type: String,
        default: "var(--primary-300)",
    },
    activeColor: {
        type: String,
        default: "var(--primary-200)",
    },
});

const hovering = ref(false);
const active = ref(false);

const computedBackgroundColor = computed(() => {
    if (props.isToggle) return "var(--secondary)"; // Use secondary color if toggled
    if (active.value) return props.activeColor;
    if (hovering.value) return props.hoverColor;
    return props.backgroundColor;
});
</script>

<style lang="scss" scoped>
.btn {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 20px;
    border-radius: 10px;
    transition: background-color 0.1s;
    user-select: none;
    white-space: nowrap;
    cursor: pointer;
}
</style>