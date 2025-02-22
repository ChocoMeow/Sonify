<template>
    <div v-show="isActive">
        <slot />
    </div>
</template>

<script setup>
import { computed, inject, onMounted } from "vue";

const props = defineProps({
    name: {
        type: String,
        required: true,
    },
    icon: {
        type: String,
        default: "",
    },
});

const addTab = inject("addTab");
const selectedTab = inject("selectedTab");

onMounted(() => {
    addTab({
        name: props.name,
        icon: props.icon,
    });
});

const isActive = computed(
    () => selectedTab && selectedTab.value === props.name
);
</script>
