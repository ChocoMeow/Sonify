<template>
    <div
        class="btn"
        :class="{ 
            toggle: isToggle, 
            disabled: disabled || isLoading,
            loading: isLoading 
        }"
        :style="{ backgroundColor: computedBackgroundColor }"
        @mouseover="!(disabled || isLoading) && (hovering = true)"
        @mouseleave="!(disabled || isLoading) && (hovering = false)"
        @mousedown="!(disabled || isLoading) && (active = true)"
        @mouseup="!(disabled || isLoading) && (active = false)"
        @click="!(disabled || isLoading) && $emit('click')"
    >
        <span v-if="!isLoading && icon" class="material-symbols-rounded fill">{{
            icon
        }}</span>
        <span v-if="isLoading" class="material-symbols-rounded loading-icon">
            sync
        </span>
        <span v-if="!isLoading">{{ name }}</span>
        <span v-else class="loading-text">Loading...</span>
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
    disabled: {
        type: Boolean,
        default: false,
    },
    isLoading: {
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

defineEmits(['click']);

const hovering = ref(false);
const active = ref(false);

const computedBackgroundColor = computed(() => {
    if (props.disabled || props.isLoading) return "var(--primary-200)"; // Disabled/loading state
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
    
    &.disabled {
        opacity: 0.6;
        cursor: not-allowed;
        
        span {
            opacity: 0.7;
        }
    }
    
    &.loading {
        cursor: wait;
    }
    
    .loading-icon {
        animation: spin 1.4s linear infinite;
    }
    
    .loading-text {
        animation: pulse 1.5s ease-in-out infinite;
    }
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes pulse {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
}
</style>