<template>
    <component 
        :is="useExternalLink ? 'a' : 'router-link'" 
        :to="useExternalLink ? undefined : {name: routeName}"
        :href="useExternalLink ? href : undefined"
        :target="newTab ? '_blank' : undefined"
        class="btn" 
        :title="name"
    >
        <!-- Material Icon -->
        <span v-if="iconType === 'material'" class="material-symbols-rounded fill">{{ icon }}</span>
        
        <!-- FontAwesome Icon -->
        <i v-else-if="iconType.startsWith('fa')" :class="`${iconType} ${icon}`"></i>
        
        <p>{{ name }}</p>
    </component>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    icon: {
        type: String,
        default: "home",
    },
    iconType: {
        type: String,
        default: "material", // 'material' or 'fa'
        validator: (value) => ['material', 'fa'].includes(value)
    },
    name: {
        type: String,
        default: "Home",
    },
    routeName: {
        type: String,
        default: null,
    },
    href: {
        type: String,
        default: null,
    },
    newTab: {
        type: Boolean,
        default: false
    }
});

// Determine if we're using a custom href (external link) or router link
const useExternalLink = computed(() => !!props.href);

// If routeName is not provided, use the lowercase name as fallback
const routeName = computed(() => props.routeName || props.name.toLowerCase());
</script>

<style lang="scss" scoped>
.btn {
    display: flex;
    gap: 12px;
    width: 100%;
    align-items: center;
    padding: 12px 20px;
    border-radius: 50px;
    cursor: pointer;
    text-decoration: none;
    color: inherit;

    &:hover {
        background-color: var(--primary-200);
    }

    &.router-link-exact-active {
        background-color: var(--primary-100);
        color: var(--primary);
    }

    p {
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    /* FontAwesome icon styling */
    i {
        font-size: 20px;
        width: 24px;
        text-align: center;
    }
}

@media screen and (max-width: 1200px) {
    .btn {
        width: fit-content;
        p {
            display: none;
        }
    }
}
</style>
