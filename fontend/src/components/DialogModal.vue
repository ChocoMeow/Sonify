<template>
    <transition name="modal">
        <div v-if="modelValue" class="modal-overlay" @click.self="close">
            <div
                class="modal-container"
                ref="modalContainer"
                tabindex="0"
                @keydown.esc="close"
            >
                <!-- @keydown.enter="submit" -->

                <div class="modal-header">
                    <RoundedButton @click="close" icon="close" name="" style="border: none; padding: 8px;"/>
                </div>
                <div class="modal-body">
                    <slot></slot>
                </div>
                <!-- <div class="modal-footer">
                    <slot name="footer">
                        <button @click="close">Cancel</button>
                        <button ref="submitButton" @click="submit">
                            Submit
                        </button>
                    </slot>
                </div> -->
            </div>
        </div>
    </transition>
</template>

<script setup>
import {
    ref,
    watch,
    onMounted,
    onUnmounted,
} from "vue";

import RoundedButton from "@/components/RoundedButton.vue";

const props = defineProps({
    modelValue: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["update:modelValue", "submit"]);
const modalContainer = ref(null);
const submitButton = ref(null);

const close = () => {
    emit("update:modelValue", false);
};

const submit = () => {
    emit("submit");
    close();
};

// Focus the modal when it opens
watch(
    () => props.modelValue,
    (newValue) => {
        if (newValue) {
            setTimeout(() => {
                modalContainer.value?.focus();
            }, 100);
        }
    }
);

// Close modal on Escape key press globally
const handleGlobalKeydown = (event) => {
    if (event.key === "Escape" && props.modelValue) {
        close();
    }
};

// Register and unregister global event listeners
onMounted(() => {
    window.addEventListener("keydown", handleGlobalKeydown);
});

onUnmounted(() => {
    window.removeEventListener("keydown", handleGlobalKeydown);
});
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(10px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999;
}

.modal-container {
    background: var(--background-2);
    border-radius: 8px;
    max-width: 700px;
    width: 90%;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 8px;
    outline: none; /* Removes default focus outline */
}

.modal-enter-active,
.modal-leave-active {
    transition: opacity 0.3s ease, transform 0.3s ease;
}
.modal-enter-from,
.modal-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}
.modal-enter-to,
.modal-leave-from {
    opacity: 1;
    transform: translateY(0);
}

.modal-header,
.modal-body,
.modal-footer {
    padding: 8px;
}
.modal-header {
    display: flex;
    justify-content:flex-end;
    align-items: center;
}
</style>