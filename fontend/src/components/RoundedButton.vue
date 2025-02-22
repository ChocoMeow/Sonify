<template>
    <div class="btn" :class="{ toggle: isToggle }">
        <span v-if="icon" class="material-symbols-rounded fill">{{
            icon
        }}</span>
        {{ name }}
    </div>
</template>

<script setup>
defineProps({
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
});
</script>

<style lang="scss" scoped>
.btn {
    display: flex;
    align-items: center;
    padding: 8px 20px;
    border: solid 1.5px var(--text);
    border-radius: 50px;
    gap: 8px;
    transition: background-color 0.1s;
    color: var(--text);
    cursor: pointer;

    &:hover {
        background-color: var(--primary-200);
    }

    &.toggle {
        background-color: var(--secondary);
    }
}
</style>
