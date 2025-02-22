<template>
    <div
        class="btn"
        :class="{ toggle: isToggle }"
        :style="{ backgroundColor: computedBackgroundColor, color: textColor}"
        @mouseover="hovering = true"
        @mouseleave="hovering = false"
        @mousedown="active = true"
        @mouseup="active = false"
    >
        <span
            v-if="icon"
            :class="['material-symbols-rounded', { fill: isFill }]"
            >{{ icon }}</span
        >
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
    isFill: {
        type: Boolean,
        default: true,
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
    textColor: {
        type: String,
        default: "var(--text)",
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
    padding: 8px;
    border-radius: 50%;
    transition: background-color 0.1s;
    user-select: none;
    cursor: pointer;
}
</style>
