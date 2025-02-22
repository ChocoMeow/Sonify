<template>
    <div class="switch" :class="{ 'switch--on': modelValue }" @click="toggle">
        <div class="switch__toggle"></div>
    </div>
</template>

<script setup>
const props = defineProps({
    modelValue: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["update:modelValue"]);

const toggle = () => {
    emit("update:modelValue", !props.modelValue);
};
</script>

<style scoped>
.switch {
    width: 50px;
    height: 24px;
    background-color: var(--primary-100);
    border-radius: 12px;
    position: relative;
    cursor: pointer;
    transition: background-color 0.2s;
}

.switch--on {
    background-color: var(--accent);
}

.switch__toggle {
    width: 19.5px;
    height: 19.5px;
    background-color: var(--text);
    border-radius: 50%;
    position: absolute;
    top: 2.5px;
    left: 2px;
    transition: transform 0.2s;
}

.switch--on .switch__toggle {
    transform: translateX(26px);
}
</style>
