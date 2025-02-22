<template>
    <div class="bar">
        <span class="material-symbols-rounded"> search </span>
        <input
            type="text"
            placeholder="Search for songs and playlists"
            v-model="searchQuery"
            @input="handleInput"
        />
    </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();
const searchQuery = ref("");

// Set the initial value of searchQuery from the route query
if (route.query.search_query) {
    searchQuery.value = route.query.search_query;
}

let timeout = null;

const handleInput = () => {
    clearTimeout(timeout);

    const trimmedQuery = searchQuery.value.trim();

    timeout = setTimeout(() => {
        if (trimmedQuery) {
            router.push({
                name: "search",
                query: { search_query: trimmedQuery },
            });
        }
    }, 1000);
};

watch(
    () => route.query.search_query,
    (newQuery) => {
        if (newQuery) {
            searchQuery.value = newQuery;
        }
    }
);
</script>

<style lang="scss" scoped>
.bar {
    display: flex;
    height: 48px;
    width: 100%;
    padding: 0 20px;
    border-radius: 16px;
    justify-content: center;
    align-items: center;
    gap: 20px;

    outline: solid 2px var(--primary-100);
    transition: outline 0.2s;

    &:hover {
        outline: solid 2px var(--primary-200);
    }

    &:focus-within {
        outline: solid 2px var(--primary);
    }

    input {
        width: 100%;
        height: 100%;
        background: none;
        outline: none;
        font-size: 15px;
        color: var(--text);
        border: none;
    }
}
</style>
